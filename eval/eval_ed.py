import os
import csv




def eval_ed(data, predictions):
    print(len(data))
    print(len(predictions))
    tp = []
    fp = []
    fn = []
    for entity1 in data:
        wb_id1 = entity1["identifier"].strip()
        if not wb_id1.startswith("Q"):
            wb_id1 = "NIL"
        for entity2 in predictions:
            if entity1["doc_id"]==entity2["doc_id"] and entity1["start_pos"]==entity2["start_pos"]:
                wb_id2 = entity2["identifier"].strip()
                if wb_id2 == wb_id1:
                    tp.append(entity2)
                else:
                    fp.append(entity2)
                    fn.append(entity1)
    accuracy = (len(tp) / (len(tp) + len(fp)))*100
    return tp, fp, fn, accuracy

path_data = "../../my_zenodo/ENEIDE/AMD/v1.0"

path_results = "./results/elite_amd_ed"

with open(os.path.join(path_data, "annotations_test.csv"), "r", encoding="utf-8") as f1:
        data = list(csv.DictReader(f1, delimiter=","))
with open(os.path.join(path_results,"output.csv"), "r", encoding="utf-8") as f2:
        predictions = list(csv.DictReader(f2, delimiter=","))


tp, fp, fn, accuracy = eval_ed(data, predictions)

data_per = [row for row in data if row["type"]=="PER"]
predictions_per = [row for row in predictions if row["type"]=="PER"]
_,_,_, per_accuracy = eval_ed(data_per, predictions_per)


data_loc = [row for row in data if row["type"]=="LOC"]
predictions_loc = [row for row in predictions if row["type"]=="LOC"]
_,_,_,loc_accuracy = eval_ed(data_loc, predictions_loc)


data_org = [row for row in data if row["type"]=="ORG"]
predictions_org = [row for row in predictions if row["type"]=="ORG"]
_,_,_,org_accuracy = eval_ed(data_org, predictions_org)

macro_accuracy = (per_accuracy + loc_accuracy + org_accuracy)/3
with open(os.path.join(path_results, "result.txt"), "w") as output:
    output.write("True Positives: " + str(len(tp)) + "\n\n")
    output.write("False Positives: " + str(len(fp)) + "\n\n")
    output.write("False Negatives: " + str(len(fn)) + "\n\n")
    output.write("Accuracy: " + str(accuracy) + "\n\n")
    output.write("Accuracy for class Person: "+ str(per_accuracy) + "\n\n")
    output.write("Accuracy for class Location: " + str(loc_accuracy) + "\n\n")
    output.write("Accuracy for class Organization: " + str(org_accuracy) + "\n\n")
    output.write("Macro-averaged Accuracy: "+str(macro_accuracy)+"\n\n")


p_keys = tp[0].keys()
fp_keys = fp[0].keys()
n_keys = fn[0].keys()

tp_file = open(os.path.join(path_results, "tp_ed.csv"), "w", encoding="utf-8")
dict_writer = csv.DictWriter(tp_file, p_keys)
dict_writer.writeheader()
dict_writer.writerows(tp)
tp_file.close()

fp_file = open(os.path.join(path_results, "fp_ed.csv"), "w", encoding="utf-8")
dict_writer = csv.DictWriter(fp_file, fp_keys)
dict_writer.writeheader()
dict_writer.writerows(fp)
fp_file.close()

fn_file = open(os.path.join(path_results, "fn_ed.csv"), "w", encoding="utf-8")
dict_writer = csv.DictWriter(fn_file, n_keys)
dict_writer.writeheader()
dict_writer.writerows(fn)
fn_file.close()


