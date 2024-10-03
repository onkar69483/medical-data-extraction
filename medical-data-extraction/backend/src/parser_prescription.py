import re
from parser_generic import MedicalDocParser


class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)

    def parse(self):
        return {
            "nature_of_illness": self.get_field("nature_of_illness"),
            "critical_findings": self.get_field("critical_findings"),
            "duration": self.get_field("duration"),
            "first_consultation_date": self.get_field("first_consultation_date"),
            "provisional_diagnosis": self.get_field("provisional_diagnosis"),
            "proposed_treatment": self.get_field("proposed_treatment"),
            "surgical_info": self.get_field("surgical_info"),
        }

    def get_field(self, field_name):
        pattern_dict = {
            "nature_of_illness": {"pattern": r"Nature of Illness / Disease with presenting complaint:([^\n]*)",
                                  "flags": 0},
            "critical_findings": {"pattern": r"Relevant Critical Findings:([^\n]*)", "flags": 0},
            "duration": {"pattern": r"Duration of the present ailment:([^\n]*)", "flags": 0},
            "first_consultation_date": {"pattern": r"Date of First consultation:\s*(\d{1,2}/\d{1,2}/\d{2,4})",
                                        "flags": 0},
            "provisional_diagnosis": {"pattern": r"Provisional diagnosis:([^\n]*)", "flags": 0},
            "proposed_treatment": {"pattern": r"Proposed line of treatment:\s*(.*)", "flags": re.DOTALL},
            "surgical_info": {"pattern": r"If surgical, name of surgery:([^\n]*)", "flags": 0},
        }

        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object["pattern"], self.text, flags=pattern_object["flags"])
            if len(matches) > 0:
                return matches[0].strip()
        return None


# Example usage
if __name__ == "__main__":
    document_text = """
    C. Nature of Illness / Disease with presenting complaint: CHRONIC LIVER DISEASE; PEDAL EDEMA, CRAMPS
    D. Relevant Critical Findings: JAUNDICE, PEDAL EDEMA
    E. Duration of the present ailment: 1 YEAR 
    i. Date of First consultation: 8/11/21
    F. Provisional diagnosis: DECOMPENSATED CHRONIC LIVER DISEASE
    G. Proposed line of treatment:
    i. Medical Management: ( )
    ii. Surgical Management: (X)
    iii. Intensive care: (X)
    H. If surgical, name of surgery: LIVER TRANSPLANTATION
    """

    pp = PrescriptionParser(document_text)
    print(pp.parse())
