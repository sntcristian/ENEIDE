import os
import csv


def eval_ed(path_data, path_results):
    with open(os.path.join(path_data, "annotations_test.csv"), "r", encoding="utf-8") as f1:
        data = list(csv.DictReader(f1, delimiter=","))
    with open(os.path.join(path_results,"output.csv"), "r", encoding="utf-8") as f2:
        predictions = list(csv.DictReader(f2, delimiter=","))

    tp = []
    fp = []
    fn = []

    for entity1, entity2 in zip(data, predictions):
        wb_id1 = entity1["identifier"].strip()
        if not wb_id1.startswith("Q"):
            continue
        else:
            wb_id2 = entity2["identifier"].strip()
            if wb_id2==wb_id1:
                tp.append(entity2)
                print(wb_id2, wb_id1)
            else:
                fp.append(entity2)
                fn.append(entity1)

    accuracy = len(tp) / (len(tp) + len(fp))
    with open(os.path.join(path_results, "result.txt"), "w") as output:
        output.write("True Positives: " + str(len(tp)) + "\n\n")
        output.write("False Positives: " + str(len(fp)) + "\n\n")
        output.write("False Negatives: " + str(len(fn)) + "\n\n")
        output.write("Accuracy: " + str(accuracy) + "\n\n")

    p_keys = tp[0].keys()
    fp_keys = fp[0].keys()
    n_keys = fn[0].keys()

    tp_file = open(os.path.join(path_results,"tp_ed.csv"), "w", encoding="utf-8")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()

    fp_file = open(os.path.join(path_results, "fp_ed.csv"), "w", encoding="utf-8")
    dict_writer = csv.DictWriter(fp_file, fp_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()

    fn_file = open(os.path.join(path_results,"fn_ed.csv"), "w", encoding="utf-8")
    dict_writer = csv.DictWriter(fn_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fn)
    fn_file.close()


eval_ed(path_data="./AMD", path_results="./disambiguation_results/AMD/blink")

