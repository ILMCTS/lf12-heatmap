from datetime import datetime
import pandas as pd
import json  # Für die JSON-Verarbeitung

class AbsenceRecord:
    """Klasse, die einen Eintrag für eine Abwesenheit darstellt."""
    
    def __init__(self, langname, vorname, id_, klasse, beginndatum, beginnzeit,
                 enddatum, endzeit, unterbrechungen, abwesenheitsgrund, 
                 text_grund, entschuldigungsnummer, status, entschuldigungstext,
                 gemeldet_von):
        self.langname = langname
        self.vorname = vorname
        self.id_ = id_
        self.klasse = klasse
        self.beginndatum = beginndatum
        self.beginnzeit = beginnzeit
        self.enddatum = enddatum
        self.endzeit = endzeit
        self.unterbrechungen = unterbrechungen
        self.abwesenheitsgrund = abwesenheitsgrund
        self.text_grund = text_grund
        self.entschuldigungsnummer = entschuldigungsnummer
        self.status = status
        self.entschuldigungstext = entschuldigungstext
        self.gemeldet_von = gemeldet_von

    def __str__(self):
        """Gibt die Informationen des Abwesenheitseintrags als String aus."""
        return (f"{self.langname} {self.vorname} ({self.id_}) - Klasse: {self.klasse}\n"
                f"Abwesenheit: {self.abwesenheitsgrund}, Grund: {self.text_grund}\n"
                f"Gemeldet von: {self.gemeldet_von}, Status: {self.status}\n"
                f"Von: {self.beginndatum} {self.beginnzeit} bis {self.enddatum} {self.endzeit}\n"
                f"Entschuldigungsnummer: {self.entschuldigungsnummer}\n"
                f"Unterbrechungen: {self.unterbrechungen}\n")

    def to_dict(self):
        """Konvertiert die Instanz in ein Dictionary."""
        return {
            "userId": self.id_, 
            "lastName": self.langname,
            "firstName": self.vorname,
            "class": self.klasse,
            "startDate": f"{str(self.beginndatum)} {str(self.beginnzeit)}",
            "endDate": f"{str(self.enddatum)} {str(self.endzeit)}",
            "status": self.abwesenheitsgrund,
            "customText": f"{str(self.text_grund)}"
        }

def read_absence_records(file_path):
    """Liest die CSV-Datei ein und gibt eine Liste von AbsenceRecord-Objekten zurück."""
    records = []
    
    # CSV-Datei einlesen
    try:
        df = pd.read_csv(file_path, sep=';', encoding='UTF-8')  
        for _, row in df.iterrows():
            record = AbsenceRecord(
                langname=row['Langname'],
                vorname=row['Vorname'],
                id_=row['ID'],
                klasse=row['Klasse'],
                beginndatum=row['Beginndatum'],
                beginnzeit=row['Beginnzeit'],
                enddatum=row['Enddatum'],
                endzeit=row['Endzeit'],
                unterbrechungen=row['Unterbrechungen'],
                abwesenheitsgrund=row['Abwesenheitsgrund'],
                text_grund=row['Text/Grund'],
                entschuldigungsnummer=row['Entschuldigungsnummer'],
                status=row['Status'],
                entschuldigungstext=row['Entschuldigungstext'],
                gemeldet_von=row['gemeldet von Schüler*in']
            )
            records.append(record)
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
    except pd.errors.EmptyDataError:
        print("Die Datei ist leer.")
    except pd.errors.ParserError:
        print("Fehler beim Parsen der Datei. Überprüfen Sie, ob die Datei im CSV-Format vorliegt.")
    
    return records

def save_records_to_json(records, json_file_path):
    """Speichert die Liste von AbsenceRecord-Objekten in eine JSON-Datei."""
    try:
        # Konvertiere jedes AbsenceRecord-Objekt in ein Dictionary
        records_dict = [record.to_dict() for record in records]
        # Speichere die Liste der Dictionaries als JSON
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(records_dict, json_file, ensure_ascii=False, indent=4)
        print(f"Die Daten wurden erfolgreich in {json_file_path} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten in JSON: {e}")

# Beispiel für die Verwendung
if __name__ == "__main__":
    # Pfad zur CSV-Datei
    file_path = "C:\\Users\\Jonas\\Downloads\\ListeAbw1.csv"
    # Zielpfad für die JSON-Datei
    json_file_path = "C:\\Users\\Jonas\\Downloads\\ListeAbw1.json"

    # Einträge aus der CSV-Datei lesen
    absence_records = read_absence_records(file_path)

    # Ausgabe der Einträge in der Konsole
    for record in absence_records:
        print(record)

    # Speichere die Daten als JSON
    save_records_to_json(absence_records, json_file_path)