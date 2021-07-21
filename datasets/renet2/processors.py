from copy import deepcopy

import pandas as pd
import pubtator
from pubtator import parse

from datasets import common
from datasets.splitters import StratifiedGroupKFold  # type: ignore

logger = common.get_logger(common.this_directory(__file__) / "logfile.log")


def load_documents(filename: str, split_by: str) -> dict[int, str]:
    """Load the documents (the docs.txt file) into a more usable dictionary format.

    Abstracts are given in a text format similar to what is returned from Pubtator, but not identical. For example:
        10234502
        Some abstract text
        $$$

        10506726
        Some abstract text
        $$$
    We split out the text and the pmids and return in a dictionary format with pmid keys and texts as values.

    Args:
        filename: The location of the data.
        split_by: What we should split on, this should either be "$$$", or "\n\n".

    Returns:

    """
    # Read and split the filename
    with open(filename, "r") as file:
        pmids_and_docs = file.read().split(split_by)

    # Split the information into lines with some neatening
    all_string_lists = [
        [s for s in abstract.split("\n") if (s not in ("", "\n", "\n\n", " "))] for abstract in pmids_and_docs
    ]
    all_string_lists = [x for x in all_string_lists if len(x) > 0]

    # Get the id and the information split by sentences
    documents = {}
    for string_list in all_string_lists:
        # Attempt to get the PMID of the document via the first line
        try:
            pmid = int(string_list[0])
        except Exception as e:
            raise Exception("Failed id conversion for sentence: {} \n\tException: {}".format(string_list, e))

        # Attempt create a document from the
        try:
            sentence = string_list[1:]
        except Exception as e:
            raise Exception("Failed sentence reduction step for: {}\n\tException: {}".format(string_list, e))

        documents[pmid] = " ".join(sentence)

    return documents


def _perform_text_replacement(annotated_abstract: pubtator.AnnotatedPubtatorAbstract, ids: list[str]) -> str:
    """Performs the text replacement i.e. -> @GENE$, @DISEASE$ for an annotated pubtator abstract.

    Args:
        annotated_abstract: Of the stated class, contains annotation and abstract information.
        ids: The list of ids to consider.

    Returns:
        A string representing the
    """
    # Ensure the ids for conversion actually exist
    assert set(ids).issubset(annotated_abstract.associated_ids), "Abstract does not hold all specified ids."

    # Perform the replacement for the specified ids, we use the @{}$ replacement as in biobert.
    text = deepcopy(annotated_abstract.text)
    for concept in annotated_abstract.concepts:
        replace_str = "@{}$".format(concept)
        string_reprs = annotated_abstract.string_representations[concept]
        for id in ids:
            if id in annotated_abstract.concept_ids[concept]:
                for string_repr in string_reprs[id]:
                    text = text.replace(string_repr, replace_str)
    return text


def build_relation_extraction_nlp_data(
    documents: dict[int, str], annotations: pd.DataFrame, labels: pd.DataFrame
) -> pd.DataFrame:
    """Converts the inputs into data that can be used to train a relation extraction model.

    This function converts the data into the form:
        index,pmid,doc,label,split
        0,1283316,"This @GENE$ effects this @DISEASE$...",1,"train"
        ...
    which is the standard relation extraction format. The data is returned as a dataframe which will be dumped as a csv.

    Arguments:
        documents: The documents for each pmid.
        annotations: The annotations relating to each documnet.
        labels: The labels of each annotation.

    Returns:
        A dataframe with (index,pmid,doc,label) columns where the doc has had the text replaced.
    """
    # This will hold (pmid, converted document, label)
    data = []

    # Each label represents a unique annotation/pmid combination so iterate over all these
    for pmid in labels["pmid"].unique():
        # Get the text and labels
        text = documents[pmid]
        labels_pmid = labels[labels["pmid"] == pmid]

        # Get the string representations of the genes and diseases
        annotation_pmid = annotations[annotations["pmid"] == pmid]
        annotation_tsv = annotation_pmid.to_csv(sep="\t", header=False, index=False).split("\n")
        if len(annotation_tsv[-1]) == 0:
            annotation_tsv.pop(-1)
        string_representations = parse._parse_annotation_lines(annotation_tsv)

        # Build the pubtator abstract class
        annotated_abstract = pubtator.AnnotatedPubtatorAbstract(
            pmid=pmid, text=text, string_representations=string_representations
        )

        # Perform the replacements
        for i, (gene_id, disease_id, label) in enumerate(labels_pmid[["geneId", "diseaseId", "label"]].values):
            # Get representation information for the gene/disease
            ids = [str(gene_id), disease_id]
            if not set(ids).issubset(annotated_abstract.associated_ids):
                logger.warning(
                    "Could not find correct associations for PMID: {}, Gene: {}, Disease: {}, Label: {}".format(
                        pmid, gene_id, disease_id, label
                    )
                )
                continue

            # Replace the representations with tags in the text
            new_text = _perform_text_replacement(annotated_abstract, ids=[str(gene_id), disease_id])

            # Add the information to data
            data.append([pmid, new_text, label])

    # Return as frame
    frame = pd.DataFrame(data=data, columns=["pmid", "doc", "label"])

    return frame


def split_train_test_val(frame: pd.DataFrame) -> pd.DataFrame:
    """Split into 5/7 train 1/7 test 1/7 val with label stratification and pmid grouping.

    The dataframe is expected to be the output of `build_relation_extraction_nlp_data` and so should be in a standard
    format. This function splits into train/val/test and adds the result as an additional column in the dataframe.

    This is not returning three dataframes, but the same dataframe with a new column denoting the splits.

    Arguments:
        frame: The dataframe returned from the `build_relation_extraction_nlp_data` function.

    Returns:
        The same dataframe but with an additional 'split' column denoting the split.
    """

    def split_once(f: pd.DataFrame, n_splits: int) -> list[int]:
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True)
        splits = list(splitter.split(f.index, f["label"].astype(int).values, groups=f["pmid"].values))
        return splits[0]

    # Split test from train/val using 7 folds
    train_val_idxs, test_idxs = split_once(frame, 7)

    # Split train val using 6 of the 6/7 remaining
    frame_train_val = frame.iloc[train_val_idxs]
    train_idxs, val_idxs = split_once(frame_train_val, 6)

    # Add the split index as a new column
    frame["split"] = None
    frame.loc[frame_train_val.iloc[train_idxs].index, "split"] = "train"
    frame.loc[frame_train_val.iloc[val_idxs].index, "split"] = "val"
    frame.loc[frame.iloc[test_idxs].index, "split"] = "test"

    # Make the index unique
    frame = frame.reset_index().drop("index", axis=1)

    return frame
