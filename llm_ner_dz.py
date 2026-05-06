import json
import csv
import argparse
import transformers
from tqdm import tqdm
import re
import torch
import os


def main():
    """Funzione principale."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Estrai entità nominate da testi usando LLM"
    )
    
    parser.add_argument(
        "--csv_path",
        type=str,
        default="./ENEIDE-data/v1.0/DZ/paragraphs_test.csv",
        help="Percorso del file CSV di input"
    )
    
    parser.add_argument(
        "--model_id",
        type=str,
        default="meta-llama/Meta-Llama-3.1-8B-Instruct",
        help="ID del modello Hugging Face"
    )
    
    parser.add_argument(
        "--hf_token",
        type=str,
        required=True,
        help="Token Hugging Face (obbligatorio)"
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        default="./results/llama_dz",
        help="Percorso della cartella di output"
    )
    

    

    system_prompt = "Sei un filologo esperto conoscitore della letteratura Italiana. Il tuo compito è quello di annotare riferimenti a Persone, Luoghi e Opere letterarie all'interno di testi storici. Generi risposte strutturate in formato JSON. Non scrivere codice Python."
    args = parser.parse_args()
    
    # Print configuration
    print("=" * 50)
    print("Estrazione Entità Nominate")
    print("=" * 50)
    print(f"CSV input: {args.csv_path}")
    print(f"Modello: {args.model_id}")
    print(f"Output: {args.output_path}")
    print("=" * 50 + "\n")
    
    # Load test data
    print("Caricamento dati...")
    with open(args.csv_path, "r", encoding="utf-8") as csv_f:
        data = csv.DictReader(csv_f)
        test_data = list(data)
    print(f"✓ Caricati {len(test_data)} record\n")
    
    # Initialize pipeline
    print("Inizializzazione modello...")
    pipeline = transformers.pipeline(
        "text-generation",
        model=args.model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
        token=args.hf_token
    )
    print("✓ Modello caricato\n")
    
    # Define instruction prompt
    instruction_prompt = """
        Estrai i riferimenti a entità nominate di tipo "persona", "luogo" e "opera" all'interno del testo in input, proveniente dalla raccolta "Zibaldone di pensieri" del poeta e filologo Giacomo Leopardi (1817 - 1832).
        Estrai le entità nella risposta utilizzando un formato JSON come nell'esempio fornito.
        Esempio di Input: "La Divina Commedia venne scritta da Dante a Firenze".
        Esempio di Output:
        ```json
            {"nome":"Divina Commedia", "tipo":"opera"},
            {"nome":"Dante", "tipo":"persona"},
            {"nome":"Firenze", "tipo":"luogo"}
        ```
        ---------------------
        Input:
        """
    
    # Extract entities
    print("Estrazione entità in corso...")
    output = []
    pattern = r'\{\s*"nome"\s*:\s*"([^"]+)"\s*,\s*"tipo"\s*:\s*"([^"]+)"\s*\}'
    
    for row in tqdm(test_data, desc="Processing rows"):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction_prompt + row["text"]},
        ]
        
        try:
            outputs = pipeline(
                messages,
                max_new_tokens=512,
            )
            
            response = outputs[0]["generated_text"][-1]["content"]
            matches = re.findall(pattern, response)
            entities = [{"nome": nome, "tipo": tipo} for nome, tipo in matches]
            
            curr_end = 0
            
            for entity in entities:
                if entity["tipo"] in {"persona", "opera", "luogo"}:
                    entity_match = re.search(re.escape(entity["nome"]), row["text"][curr_end:])
                    
                    if entity_match:
                        start_pos = curr_end + entity_match.start()
                        end_pos = curr_end + entity_match.end()
                        
                        output_entry = {
                            "id": row["doc_id"],
                            "surface_form": entity["nome"],
                            "start_pos": start_pos,
                            "end_pos": end_pos,
                            "type": entity["tipo"]
                        }
                        output.append(output_entry)
                        curr_end = end_pos
                        
        except Exception as e:
            print(f"Errore processing row {row.get('id', 'unknown')}: {e}")
            continue
    
    # Save results
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    
    if output:
        keys = output[0].keys()
        output_file = os.path.join(args.output_path, "output.csv")
        
        with open(output_file, "w", encoding="utf-8", newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(output)
        
        print(f"\n✓ Risultati salvati in: {output_file}")
        print(f"✓ Entità estratte: {len(output)}")
    else:
        print("\n⚠ Nessuna entità estratta.")


if __name__ == "__main__":
    main()