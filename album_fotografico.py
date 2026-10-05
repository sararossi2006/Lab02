import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = {}
    try:
        #apro il file in lettura, uso with così evito di dimenticare la chiusura
        with open(file_path, "r", encoding = "utf-8") as infile:
            reader = csv.reader(infile)

            prima_riga = True
            for row in reader:
                if prima_riga:
                    prima_riga = False
                    continue
                if len(row) == 5:
                    codice = row[0].strip()
                    titolo = row[1].strip()
                    autore = row[2].strip()
                    mese = int(row[3].strip())
                    anno = int(row[4].strip())
                    foto = {
                        'codice' : codice,
                        'titolo' : titolo,
                        'autore' : autore,
                        'mese' : mese,
                        'anno' : anno
                    }
                    # se l'anno non esiste, creo la chiave nel dizionario associata a una lista vuota
                    if anno not in album:
                        album[anno] = []
                    album[anno].append(foto) #aggiungo la foto alla lista dell'anno
    except FileNotFoundError:
        return None # restituisco None se il file non si trova
    return album
    # TODO


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12: #controllo che il mese sia valido
        return None
    #ora controllo che il codice non esista già girando sulle foto esistenti
    for anno_esistente in album:
        for f in album[anno_esistente]:
            if f['codice'] == codice:
                return None

    nuova_foto = {
        'codice' : codice,
        'titolo' : titolo,
        'autore' : autore,
        'mese' : mese,
        'anno' : anno
    }

    # affiorno il file CSV con append
    try:
        with open(file_path, "a", encoding = "utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([codice, titolo, autore, mese, anno])
    except FileNotFoundError:
        return None

    #aggiorno il dizionario in memoria
    if anno not in album:
        album[anno] = []
    album[anno].append(nuova_foto)
    return nuova_foto

    # TODO


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno in album:
        for foto in album[anno]:
            if foto['codice'] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:
        return None #l'anno non è mai comparso
    #creo la lista dei titoli con un ciclo for
    titoli = []
    for foto in album[anno]:
        titoli.append(foto['titolo'])
    #ora ordino la lista  in ordine alfabetico
    titoli.sort()
    return titoli

    # TODO


def main():
    album = {}  #ho cambiato l'inizializzazione in album = {}
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
