# Order to run the scripts

1. sample_data.py (get text and annotations in csv from html and divide in 75/15/15 ratio)
2. OPTIONAL: get_surface_forms.py (get surface forms used in AMD to be manually validated)
3. OPTIONAL: get_extra_annotations.py (get supplementary annotations automatically extracted for manual validation)ù
4. OPTIONAL: merge_annotations.py (merge manual annotations with automatically extracted annotations)
5. OPTIONAL: refine_dates.py (get more precise dates using AMD turtle Knowledge Base)