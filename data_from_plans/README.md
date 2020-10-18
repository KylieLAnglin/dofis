To create exemptions and implementation data dataset, notebooks should be run in the following order:

1. gather_documents_notebook
2. clean_documents_notebook
3. train_doc_classifier_notebook
4. narrow_documents_notebook
5. extract_laws_notebook
6. train_date_term_classifier_notebook
7. train_date_finalize_classifier_notebook
8. extract_dates_notebook
9. replace_missing_notebook
10. one_hot_save_and_clean_notebook