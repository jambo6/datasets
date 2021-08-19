# HMDD

## Dataset summary
A microRNA-disease association database. The full text for the v3.0 version of the database can be found [here](https://watermark.silverchair.com/gky1010.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAAsMwggK_BgkqhkiG9w0BBwagggKwMIICrAIBADCCAqUGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMBL5_5OruZxC8tgCgAgEQgIICdqL_K4H01cKeyVmVdoouLSYOY89twJJM3eB8GwuYuQlaDb-uWYJt9GoKBxslTMK7eTWqH-cXzogIdL-U5nRgnYsVFOIYURIZajfXjApyC-yTGFnSlAZbaJlZAjbTx7ts0QlOXAkilC9vFc-1JbIdvsIITQAQR7J_b1JKF17wiIxwB_W4cLoB0VEbC1qDn9oRPVtppqfySSwv-BKfIuBvE3mucXsmPAl0sMrdWBp1cqdXLPspgfBKu3V0Q-uozNhEr3A4skzyy4-Lo0MgNnWiBmMKkJOjtrbPGCY3O9dnGkAQ1zurtJXKUuMQwG1i_ae_bX0hYlCYhA0c4fwl5QXCNizSUomDvdI2ZqcUcIc_q-qSEN4XAW0oGkct7tYJPeTdkfvHBi2eqxl1QMHgI81MaWINOJY_VYvX2X_B_gVkct3vB8tBake3Qn0rICjTM4KyCIcc0p3fasfa6WewSPJZBlMZk3M_7pKiPKpi_KNr5X3BFUKsLs1VXNyy-3ni7M_Xmo9VNsHS6siD8Nitc3tCcXVgZQ9xGgp5mYQk1VuGDOZuw7cj9bM6X9mC5aFlCjpESiwxKofEFkS5ZgGRz46k0uvEijvB0t1Pp-Ce7QaJZwH7q6Rq57aCqR-Lr6Pa2DZzhY81QIa-rBg7_Lj9x89d_4p_oWj0dZ7-bYMyByyAyzUCl8bidMygCUQgtCEl5sSTnTJ8hsNxJaeZ0L9CQ4ZpV1kkXVYWmPMkbKgdsvWo-CIl9Swy0-Xqx-ekhANTdmgenTn5ZFrl2biNQBHdYbc5Pso4ZZIvISr3IfOi-iV5nqYdLd7D2prqp7oejzx_z6H4bdQ3ptTxWQ).

### Processed folder
The processed folder will contain two files, `alldata.csv` and `overview.csv`.

`alldata.csv` contains all relationships between miRNA and diseases that includes

- Sentences that determined the relationships
- Causality of non-causality of the relationships
- pmids/meshIDs/etc.

`overview.csv` contains a pre-complied statistical overview of each miRNA against the diseases. The included categories are:

- **cdn** The number of diseases the miRNA has been found to be causal to.
- **dsw** The number of diseases associated to the miRNA divided by the total number of diseases associated to all miRNAs.
- **fmn** The number of family members (miRNAs can be classified in families with similar structures; see for example [this paper](https://www.nature.com/articles/srep02940).
- **snp** The number of single nucleotide polymorphisms (SNPs) contained in miRNA precursors.

### Link

http://www.cuilab.cn/hmdd/

### Citation

```angular2html
@article{huang2019hmdd,
  title={HMDD v3. 0: a database for experimentally supported human microRNA--disease associations},
  author={Huang, Zhou and Shi, Jiangcheng and Gao, Yuanxu and Cui, Chunmei and Zhang, Shan and Li, Jianwei and Zhou, Yuan and Cui, Qinghua},
  journal={Nucleic acids research},
  volume={47},
  number={D1},
  pages={D1013--D1017},
  year={2019},
  publisher={Oxford University Press}
}
```

