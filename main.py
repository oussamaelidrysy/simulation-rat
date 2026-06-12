import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import threading

"""
GESTION DES GERMES
"""
class GenerateurAlea:
    def __init__(self, ix, iy, iz):
        self.IX = ix
        self.IY = iy
        self.IZ = iz

    def alea(self):
        self.IX = 171*(self.IX % 177) - 2*(self.IX // 177)
        self.IY = 172*(self.IY % 176) - 35*(self.IY // 176)
        self.IZ = 170*(self.IZ % 178) - 63*(self.IZ // 178)

        if self.IX < 0: self.IX += 30269
        if self.IY < 0: self.IY += 30307
        if self.IZ < 0: self.IZ += 30323

        inter = (self.IX/30269) + (self.IY/30307) + (self.IZ/30323)
        return round(inter - int(inter), 4)

# """
# FONCTIONS UTILITAIRES
# """
# def alea ():
#     inter:float
#     global IX, IY, IZ

#     IX = 171*(IX%177) - 2*(IX//177)
#     IY = 172*(IY%176) - 35*(IY//176)
#     IZ = 170*(IZ%178) - 63*(IZ//178)

#     if IX<0:
#         IX=IX+30269
#     if IY<0:
#         IY=IY+30307
#     if IZ<0:
#         IZ=IZ+30323

#     inter = ((IX/30269)+(IY/30307)+(IZ/30323))
#     # print(f"IX: {IX}, IY: {IY}, IZ: {IZ}")
#     return round(inter - int(inter),4)

"""
DECLARATION DES CLASSES
"""
class Employe:
    def __init__(self, scenario, gen):
        self.scenario = scenario
        self.gen = gen
        self.genre = self.initialiser_genre()
        self.age = self.initialiser_age()
        self.age_embauche = self.initialiser_age_embauche()
        self.salaire = self.initialiser_salaire()
        self.cotisation = self.calculer_cotisation()
        self.NAST = 0

    def initialiser_genre(self):
        return "Homme" if self.gen.alea() <= 0.55 else "Femme"
    
    def initialiser_age(self):
        na_1 = self.gen.alea()
        na_2 = self.gen.alea()

        if na_1 < 0.2:
            return 21+int(na_2*10)
        elif na_1 < 0.5:
            return 31+int(na_2*10)
        elif na_1 < 0.8:
            return 41+int(na_2*12)
        else:
            return 53+int(na_2*11)

    def initialiser_age_embauche(self):
        na_1 = self.gen.alea()
        na_2 = self.gen.alea()
        if na_1 < 0.05:
            return 21+int(na_2*4)
        elif na_1 <= 0.35:
            return 25+int(na_2*4)
        elif na_1 <= 0.65:
            return 29+int(na_2*4)
        elif na_1 <= 0.80:
            return 33+int(na_2*4)
        elif na_1 <= 0.95:
            return 37+int(na_2*4)
        else:
            return 41+int(na_2*4)
        
    def initialiser_salaire(self):
        na_1 = self.gen.alea()
        na_2 = self.gen.alea()
        if na_1 < 0.16:
            return 3000 + int(na_2*2000)
        elif na_1 <= 0.36:
            return 5000 + int(na_2*2500)
        elif na_1 <= 0.56:
            return 7500 + int(na_2*2500)
        elif na_1 <= 0.76:
            return 10000 + int(na_2*5000)
        elif na_1 <= 0.86:
            return 15000 + int(na_2*5000)
        elif na_1 <= 0.91:
            return 20000 + int(na_2*10000)
        elif na_1 <= 0.96:
            return 30000 + int(na_2*10000)
        elif na_1 <= 0.99:
            return 40000 + int(na_2*40001)
        else:
            return 80001 + int(na_2*10000)

    def calculer_cotisation(self):
        if self.scenario == 1:
            if self.salaire < 5000:
                return self.salaire * 0.05
            elif self.salaire < 7000:
                return self.salaire * 0.06
            elif self.salaire <= 10000:
                return self.salaire * 0.08
            else:
                return self.salaire * 0.1
        else: # Scénario 2
            if self.salaire < 5000:
                cotis_employe = self.salaire * 0.06
                cotis_employeur = self.salaire * 0.06
                return cotis_employe + cotis_employeur
            elif self.salaire < 7000:
                cotis_employe = self.salaire * 0.07
                cotis_employeur = self.salaire * 0.07
                return cotis_employe + cotis_employeur
            elif self.salaire <= 10000:
                cotis_employe = self.salaire * 0.08
                cotis_employeur = self.salaire * 0.08
                return cotis_employe + cotis_employeur
            else:
                cotis_employe = self.salaire * (min(0.3, (10 + (self.salaire%10000)*2)))
                cotis_employeur = self.salaire * (min(0.3, (10 + (self.salaire%10000)*2)))
                return cotis_employe + cotis_employeur

    def changer_salaire(self, nouveau_salaire):
        self.salaire = nouveau_salaire
        self.cotisation = self.calculer_cotisation()

    def prolonger_activite(self):
        if self.age < 70:
            if self.age >= 63:
                if self.salaire >= 30000:
                    if self.genre=="Homme" and self.gen.alea() <= (0.7-(self.NAST*0.05)):
                        self.NAST += 1
                        return True
                    elif self.genre=="Femme" and self.gen.alea() <= (0.5-(self.NAST*0.04)):
                        self.NAST += 1
                        return True
                    else:                    
                        return False
                elif self.salaire >= 10000:
                    if self.genre=="Homme" and self.gen.alea() <= (0.5-(self.NAST*0.04)):
                        self.NAST += 1
                        return True
                    elif self.genre=="Femme" and self.gen.alea() <= (0.3-(self.NAST*0.02)):
                        self.NAST += 1
                        return True
                    else:                    
                        return False
                elif self.salaire >= 5000:
                    if self.genre=="Homme" and self.gen.alea() <= (0.3-(self.NAST*0.02)):
                        self.NAST += 1
                        return True
                    elif self.genre=="Femme" and self.gen.alea() <= (0.15-(self.NAST*0.01)):
                        self.NAST += 1
                        return True
                    else:                    
                        return False
                else:
                    if self.genre=="Homme" and self.gen.alea() <= (0.1-(self.NAST*0.01)):
                        self.NAST += 1
                        return True
                    elif self.genre=="Femme" and self.gen.alea() <= (0.05-(self.NAST*0.01)):
                        self.NAST += 1
                        return True
                    else:                    
                        return False
            else:
                return True # Prolongation d'activité par défaut pourles employés de moins de 63 ans
        else:
            return False # Pas de prolongation d'activité possible pour les employés passé 70 ans
            

    @property
    def salaire_str(self):
        return f"{self.salaire}dh"
    
    @property
    def cotisation_str(self):
        return f"{self.cotisation}dh"
        

class Pensionnaire:
    def __init__(self, DSAR, NAT):
        self.pension = ((NAT * 2) / 100) * DSAR

    @classmethod
    def initialisation(cls, gen):
        DSAR = cls.initialiser_dsar(gen)
        NAT = cls.initialiser_nat(gen)
        return cls(DSAR, NAT)
    
    @staticmethod
    def initialiser_dsar(gen):
        na_1 = gen.alea()
        na_2 = gen.alea()
        if na_1 < 0.16:
            return 3000 + int(na_2*2000)
        elif na_1 <= 0.36:
            return 5000 + int(na_2*2500)
        elif na_1 <= 0.56:
            return 7500 + int(na_2*2500)
        elif na_1 <= 0.76:
            return 10000 + int(na_2*5000)
        elif na_1 <= 0.86:
            return 15000 + int(na_2*5000)
        elif na_1 <= 0.91:
            return 20000 + int(na_2*10000)
        elif na_1 <= 0.96:
            return 30000 + int(na_2*10000)
        elif na_1 <= 0.99:
            return 40000 + int(na_2*40001)
        else:
            return 80001 + int(na_2*10000)
        
    @staticmethod
    def initialiser_nat(gen):
        na_1 = gen.alea()
        na_2 = gen.alea()
        if na_1 < 0.05:
            return 63 - (21+int(na_2*4))
        elif na_1 <= 0.35:
            return 63 - (25+int(na_2*4))
        elif na_1 <= 0.65:
            return 63 - (29+int(na_2*4))
        elif na_1 <= 0.80:
            return 63 - (33+int(na_2*4))
        elif na_1 <= 0.95:
            return 63 - (37+int(na_2*4))
        else:
            return 63 - (41+int(na_2*4))

    @property
    def pension_str(self):
        return f"{self.pension}dh"
    


"""
SCENARII
"""
def scenario_1(gen):
    # print("\n------ Scénario 1 ------")
    columns = ["Année", "TotEmp", "TotRet", "TotCotis", "TotPens", "Reserve", "NouvRet", "NouvRec"]
    bilans_annuels = []

    reserve = 200000000
    adherents = [Employe(1, gen) for _ in range(10000)]
    pensionnaires = [Pensionnaire.initialisation(gen) for _ in range(3000)]
    for annee in range(2026, 2036):
        # print(f"\nAnnée {annee}:")

        # Mis à jour des salaires (janvier)
        if annee in [2026, 2030, 2034]: # Augmentation de 5% tous les 4 ans
            for adherent in adherents:
                adherent.changer_salaire(adherent.salaire * 1.05)
                adherent.cotisation = adherent.calculer_cotisation() # Recalcul de la cotisation après augmentation de salaire

        # Mis à jour de l'âge des adhérents (courant de l'année)
        for adherent in adherents:
            adherent.age += 1

        # Calcul des cotisations et pensions (décembre)
        total_cotisations = sum(adherent.cotisation for adherent in adherents)
        total_pensions = sum(pensionnaire.pension for pensionnaire in pensionnaires)
        reserve += total_cotisations - total_pensions
        # print(f"Total cotisations: {total_cotisations}dh")
        # print(f"Total pensions: {total_pensions}dh")
        # print(f"Réserve: {reserve}dh")

        # Comptage des employés et pensionnaires avant mise à jour
        TotEmp = len(adherents)
        TotRet = len(pensionnaires)

        # Passage à la retraite ?
        nouvRet = 0
        for adherent in adherents:
            if adherent.age >= 63:
                nouvRet += 1
                pensionnaires.append(Pensionnaire(adherent.salaire, 63 - adherent.age_embauche))
                adherents.remove(adherent)
        
        # Recrutement de nouveaux employés
        nouvRec = 250 + int(gen.alea()*151)
        adherents.extend([Employe(1, gen) for _ in range(nouvRec)])

        bilans_annuels.append({
            "Année": annee,
            "TotEmp": TotEmp,
            "TotRet": TotRet,
            "TotCotis": round(total_cotisations / 1_000_000, 3),
            "TotPens":  round(total_pensions    / 1_000_000, 3),
            "Reserve":  round(reserve            / 1_000_000, 3),
            "NouvRet": nouvRet,
            "NouvRec": nouvRec
        })

    bilan = pd.DataFrame(bilans_annuels, columns=columns)
    return bilan

def scenario_2(gen):
    # print("\n------ Scénario 2 ------")
    columns = ["Année", "TotEmp", "Plus63", "Plus63H", "Plus63F", "TotRet", "TotCotis", "TotPens", "Reserve", "NouvRet", "NouvRec"]
    bilans_annuels = []

    reserve = 200000000
    adherents = [Employe(2, gen) for _ in range(10000)]
    pensionnaires = [Pensionnaire.initialisation(gen) for _ in range(3000)]
    for annee in range(2026, 2036):
        # print(f"\nAnnée {annee}:")

        # Mis à jour des salaires (janvier)
        if annee in [2028, 2030, 2032, 2034]: # Augmentation de 10% tous les 2 ans
            for adherent in adherents:
                adherent.changer_salaire(adherent.salaire * 1.10)
                adherent.cotisation = adherent.calculer_cotisation() # Recalcul de la cotisation après augmentation de salaire
        
        # Mis à jour de l'âge des adhérents (courant de l'année)
        for adherent in adherents:
            adherent.age += 1

        # Calcul des cotisations et pensions (décembre)
        total_cotisations = sum(adherent.cotisation for adherent in adherents)
        total_pensions = sum(pensionnaire.pension for pensionnaire in pensionnaires)
        reserve += total_cotisations - total_pensions
        # print(f"Total cotisations: {total_cotisations}dh")
        # print(f"Total pensions: {total_pensions}dh")
        # print(f"Réserve: {reserve}dh")

        # Comptage des employés et pensionnaires avant mise à jour
        TotEmp = len(adherents)
        TotRet = len(pensionnaires)

        # Passage à la retraite ?
        nouvRet = 0
        for adherent in adherents:
            # Tester l'envie de chaque employé de plus de 63 ans
            if adherent.age >= 63:
                if adherent.prolonger_activite():
                    continue
                else:
                    nouvRet += 1
                    pensionnaires.append(Pensionnaire(adherent.salaire, (63 - adherent.age_embauche)+adherent.NAST))
                    adherents.remove(adherent)
        
        # Recrutement de nouveaux employés
        nouvRec = 300 + int(gen.alea()*301) # Recrutement plus important que dans le scénario 1
        adherents.extend([Employe(2, gen) for _ in range(nouvRec)])

        bilans_annuels.append({
            "Année": annee,
            "TotEmp": TotEmp,
            "Plus63": sum(1 for adherent in adherents if adherent.age >= 63),
            "Plus63H": sum(1 for adherent in adherents if adherent.age >= 63 and adherent.genre == "Homme"),
            "Plus63F": sum(1 for adherent in adherents if adherent.age >= 63 and adherent.genre == "Femme"),
            "TotRet": TotRet,
            "TotCotis": round(total_cotisations / 1_000_000, 3),
            "TotPens":  round(total_pensions    / 1_000_000, 3),
            "Reserve":  round(reserve            / 1_000_000, 3),
            "NouvRet": nouvRet,
            "NouvRec": nouvRec
        })

    bilan = pd.DataFrame(bilans_annuels, columns=columns)
    return bilan

def _une_simulation_s1(i, ix, iy, iz):
    """Une simulation isolée avec son propre générateur."""
    gen = GenerateurAlea(ix + (i+1)*5, iy + (i+1)*5, iz + (i+1)*5)
    return i, scenario_1(gen)

def n_fois_scenario_1(n, ix_init, iy_init, iz_init):
    # print("\n------ {}x Scénario 1 ------".format(n))
    columns = ["TotEmp", "TotRet", "TotCotis", "TotPens", "Reserve", "NouvRet", "NouvRec"]
    
    resultats = [None] * n

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(_une_simulation_s1, i, ix_init, iy_init, iz_init)
            for i in range(n)
        ]
        for future in futures:
            i, bilan = future.result()
            resultats[i] = bilan
    
    bilan_2026 = pd.DataFrame(columns=columns)
    bilan_2030 = pd.DataFrame(columns=columns)
    bilan_2035 = pd.DataFrame(columns=columns)

    bilan_reserve = pd.DataFrame(columns=["Reserve_2026", "Reserve_2027", "Reserve_2028", "Reserve_2029", "Reserve_2030", "Reserve_2031", "Reserve_2032", "Reserve_2033", "Reserve_2034", "Reserve_2035"])


    for i, bilan in enumerate(resultats):

        nouvelle_ligne = {
            "Simulation": i+1,
            "TotEmp": bilan.loc[bilan["Année"] == 2026, "TotEmp"].values[0],
            "TotRet": bilan.loc[bilan["Année"] == 2026, "TotRet"].values[0],
            "TotCotis": bilan.loc[bilan["Année"] == 2026, "TotCotis"].values[0],
            "TotPens": bilan.loc[bilan["Année"] == 2026, "TotPens"].values[0],
            "Reserve": bilan.loc[bilan["Année"] == 2026, "Reserve"].values[0],
            "NouvRet": bilan.loc[bilan["Année"] == 2026, "NouvRet"].values[0],
            "NouvRec": bilan.loc[bilan["Année"] == 2026, "NouvRec"].values[0]
        }
        bilan_2026 = pd.concat([bilan_2026, pd.DataFrame([nouvelle_ligne])], ignore_index=True)

        nouvelle_ligne = {
            "Simulation": i+1,
            "TotEmp": bilan.loc[bilan["Année"] == 2030, "TotEmp"].values[0],
            "TotRet": bilan.loc[bilan["Année"] == 2030, "TotRet"].values[0],
            "TotCotis": bilan.loc[bilan["Année"] == 2030, "TotCotis"].values[0],
            "TotPens": bilan.loc[bilan["Année"] == 2030, "TotPens"].values[0],
            "Reserve": bilan.loc[bilan["Année"] == 2030, "Reserve"].values[0],
            "NouvRet": bilan.loc[bilan["Année"] == 2030, "NouvRet"].values[0],
            "NouvRec": bilan.loc[bilan["Année"] == 2030, "NouvRec"].values[0]
        }
        bilan_2030 = pd.concat([bilan_2030, pd.DataFrame([nouvelle_ligne])], ignore_index=True)

        nouvelle_ligne = {
            "Simulation": i+1,
            "TotEmp": bilan.loc[bilan["Année"] == 2035, "TotEmp"].values[0],
            "TotRet": bilan.loc[bilan["Année"] == 2035, "TotRet"].values[0],
            "TotCotis": bilan.loc[bilan["Année"] == 2035, "TotCotis"].values[0],
            "TotPens": bilan.loc[bilan["Année"] == 2035, "TotPens"].values[0],
            "Reserve": bilan.loc[bilan["Année"] == 2035, "Reserve"].values[0],
            "NouvRet": bilan.loc[bilan["Année"] == 2035, "NouvRet"].values[0],
            "NouvRec": bilan.loc[bilan["Année"] == 2035, "NouvRec"].values[0]
        }
        bilan_2035 = pd.concat([bilan_2035, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
        
        nouvelle_ligne_reserve = {
            "Simulation": i+1,
            "Reserve_2026": bilan.loc[bilan["Année"] == 2026, "Reserve"].values[0],
            "Reserve_2027": bilan.loc[bilan["Année"] == 2027, "Reserve"].values[0],
            "Reserve_2028": bilan.loc[bilan["Année"] == 2028, "Reserve"].values[0],
            "Reserve_2029": bilan.loc[bilan["Année"] == 2029, "Reserve"].values[0],
            "Reserve_2030": bilan.loc[bilan["Année"] == 2030, "Reserve"].values[0],
            "Reserve_2031": bilan.loc[bilan["Année"] == 2031, "Reserve"].values[0],
            "Reserve_2032": bilan.loc[bilan["Année"] == 2032, "Reserve"].values[0],
            "Reserve_2033": bilan.loc[bilan["Année"] == 2033, "Reserve"].values[0],
            "Reserve_2034": bilan.loc[bilan["Année"] == 2034, "Reserve"].values[0],
            "Reserve_2035": bilan.loc[bilan["Année"] == 2035, "Reserve"].values[0]
         }
        bilan_reserve = pd.concat([bilan_reserve, pd.DataFrame([nouvelle_ligne_reserve])], ignore_index=True)
    
    bilan_2026 = bilan_2026.set_index("Simulation")
    bilan_2030 = bilan_2030.set_index("Simulation")
    bilan_2035 = bilan_2035.set_index("Simulation")
    bilan_reserve = bilan_reserve.set_index("Simulation")

    moyennes_2026 = bilan_2026.mean().rename("Moyenne")
    moyennes_2030 = bilan_2030.mean().rename("Moyenne")
    moyennes_2035 = bilan_2035.mean().rename("Moyenne")
    moyennes_reserve = bilan_reserve.mean().rename("Moyenne")

    bilan_2026_final = pd.concat([bilan_2026, moyennes_2026.to_frame().T], axis=0)
    bilan_2030_final = pd.concat([bilan_2030, moyennes_2030.to_frame().T], axis=0)
    bilan_2035_final = pd.concat([bilan_2035, moyennes_2035.to_frame().T], axis=0)
    bilan_reserve_final = pd.concat([bilan_reserve, moyennes_reserve.to_frame().T], axis=0)

    return bilan_2026_final, bilan_2030_final, bilan_2035_final, bilan_reserve_final

def _une_simulation_s2(i, ix, iy, iz):
    """Une simulation isolée avec son propre générateur."""
    gen = GenerateurAlea(ix + (i+1)*5, iy + (i+1)*5, iz + (i+1)*5)
    return i, scenario_2(gen)

def n_fois_scenario_2(n, ix_init, iy_init, iz_init):
    # print("\n------ {}x Scénario 2 ------".format(n))
 
    columns = ["TotEmp", "Plus63", "Plus63H", "Plus63F", "TotRet", "TotCotis", "TotPens", "Reserve", "NouvRet", "NouvRec"]
    
    resultats = [None] * n

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(_une_simulation_s2, i, ix_init, iy_init, iz_init)
            for i in range(n)
        ]
        for future in futures:
            i, bilan = future.result()
            resultats[i] = bilan
    
    bilan_2026 = pd.DataFrame(columns=columns)
    bilan_2030 = pd.DataFrame(columns=columns)
    bilan_2035 = pd.DataFrame(columns=columns)

    bilan_reserve = pd.DataFrame(columns=["Reserve_2026", "Reserve_2027", "Reserve_2028", "Reserve_2029", "Reserve_2030", "Reserve_2031", "Reserve_2032", "Reserve_2033", "Reserve_2034", "Reserve_2035"])

    for i, bilan in enumerate(resultats):

        nouvelle_ligne = {
            "Simulation": i+1,
            "TotEmp": bilan.loc[bilan["Année"] == 2026, "TotEmp"].values[0],
            "Plus63": bilan.loc[bilan["Année"] == 2026, "Plus63"].values[0],
            "Plus63H": bilan.loc[bilan["Année"] == 2026, "Plus63H"].values[0],
            "Plus63F": bilan.loc[bilan["Année"] == 2026, "Plus63F"].values[0],
            "TotRet": bilan.loc[bilan["Année"] == 2026, "TotRet"].values[0],
            "TotCotis": bilan.loc[bilan["Année"] == 2026, "TotCotis"].values[0],
            "TotPens": bilan.loc[bilan["Année"] == 2026, "TotPens"].values[0],
            "Reserve": bilan.loc[bilan["Année"] == 2026, "Reserve"].values[0],
            "NouvRet": bilan.loc[bilan["Année"] == 2026, "NouvRet"].values[0],
            "NouvRec": bilan.loc[bilan["Année"] == 2026, "NouvRec"].values[0]
        }
        bilan_2026 = pd.concat([bilan_2026, pd.DataFrame([nouvelle_ligne])], ignore_index=True)

        nouvelle_ligne = {
            "Simulation": i+1,
            "TotEmp": bilan.loc[bilan["Année"] == 2030, "TotEmp"].values[0],
            "Plus63": bilan.loc[bilan["Année"] == 2030, "Plus63"].values[0],
            "Plus63H": bilan.loc[bilan["Année"] == 2030, "Plus63H"].values[0],
            "Plus63F": bilan.loc[bilan["Année"] == 2030, "Plus63F"].values[0],
            "TotRet": bilan.loc[bilan["Année"] == 2030, "TotRet"].values[0],
            "TotCotis": bilan.loc[bilan["Année"] == 2030, "TotCotis"].values[0],
            "TotPens": bilan.loc[bilan["Année"] == 2030, "TotPens"].values[0],
            "Reserve": bilan.loc[bilan["Année"] == 2030, "Reserve"].values[0],
            "NouvRet": bilan.loc[bilan["Année"] == 2030, "NouvRet"].values[0],
            "NouvRec": bilan.loc[bilan["Année"] == 2030, "NouvRec"].values[0]
        }
        bilan_2030 = pd.concat([bilan_2030, pd.DataFrame([nouvelle_ligne])], ignore_index=True)

        nouvelle_ligne = {
            "Simulation": i+1,
            "TotEmp": bilan.loc[bilan["Année"] == 2035, "TotEmp"].values[0],
            "Plus63": bilan.loc[bilan["Année"] == 2035, "Plus63"].values[0],
            "Plus63H": bilan.loc[bilan["Année"] == 2035, "Plus63H"].values[0],
            "Plus63F": bilan.loc[bilan["Année"] == 2035, "Plus63F"].values[0],
            "TotRet": bilan.loc[bilan["Année"] == 2035, "TotRet"].values[0],
            "TotCotis": bilan.loc[bilan["Année"] == 2035, "TotCotis"].values[0],
            "TotPens": bilan.loc[bilan["Année"] == 2035, "TotPens"].values[0],
            "Reserve": bilan.loc[bilan["Année"] == 2035, "Reserve"].values[0],
            "NouvRet": bilan.loc[bilan["Année"] == 2035, "NouvRet"].values[0],
            "NouvRec": bilan.loc[bilan["Année"] == 2035, "NouvRec"].values[0]
        }
        bilan_2035 = pd.concat([bilan_2035, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
        
        nouvelle_ligne_reserve = {
            "Simulation": i+1,
            "Reserve_2026": bilan.loc[bilan["Année"] == 2026, "Reserve"].values[0],
            "Reserve_2027": bilan.loc[bilan["Année"] == 2027, "Reserve"].values[0],
            "Reserve_2028": bilan.loc[bilan["Année"] == 2028, "Reserve"].values[0],
            "Reserve_2029": bilan.loc[bilan["Année"] == 2029, "Reserve"].values[0],
            "Reserve_2030": bilan.loc[bilan["Année"] == 2030, "Reserve"].values[0],
            "Reserve_2031": bilan.loc[bilan["Année"] == 2031, "Reserve"].values[0],
            "Reserve_2032": bilan.loc[bilan["Année"] == 2032, "Reserve"].values[0],
            "Reserve_2033": bilan.loc[bilan["Année"] == 2033, "Reserve"].values[0],
            "Reserve_2034": bilan.loc[bilan["Année"] == 2034, "Reserve"].values[0],
            "Reserve_2035": bilan.loc[bilan["Année"] == 2035, "Reserve"].values[0]
         }
        bilan_reserve = pd.concat([bilan_reserve, pd.DataFrame([nouvelle_ligne_reserve])], ignore_index=True)
    
    bilan_2026 = bilan_2026.set_index("Simulation")
    bilan_2030 = bilan_2030.set_index("Simulation")
    bilan_2035 = bilan_2035.set_index("Simulation")
    bilan_reserve = bilan_reserve.set_index("Simulation")

    moyennes_2026 = bilan_2026.mean().rename("Moyenne")
    moyennes_2030 = bilan_2030.mean().rename("Moyenne")
    moyennes_2035 = bilan_2035.mean().rename("Moyenne")
    moyennes_reserve = bilan_reserve.mean().rename("Moyenne")

    bilan_2026_final = pd.concat([bilan_2026, moyennes_2026.to_frame().T], axis=0)
    bilan_2030_final = pd.concat([bilan_2030, moyennes_2030.to_frame().T], axis=0)
    bilan_2035_final = pd.concat([bilan_2035, moyennes_2035.to_frame().T], axis=0)
    bilan_reserve_final = pd.concat([bilan_reserve, moyennes_reserve.to_frame().T], axis=0)

    return bilan_2026_final, bilan_2030_final, bilan_2035_final, bilan_reserve_final


"""
FONCTION PRINCIPALE
"""
def main():
    print("CECI EST UNE INTERFACE DE TEST. POUR UNE UTILISATION OPTIMALE, EXECUTEZ LA COMMANDE 'streamlit run app.py' DANS VOTRE TERMINAL\n")
    print("Initialisation des germes...\n")
    print("Entrez les germes IX, IY et IZ (entiers positifs) :")
    IX = int(input("\nIX: "))
    IY = int(input("\nIY: "))
    IZ = int(input("\nIZ: "))
    print("\nGermes initialisés.")
    
    while(1):
        print("\nChoix du scénario...")
        scenario = int(input("\nEntrez '1' ou '2' ou '3' ou '4':"))
        if scenario in [1, 2, 3, 4]:
            break
        else:
            print("\nScénario invalide.")

    if scenario == 1:
        bilan = scenario_1(GenerateurAlea(IX, IY, IZ))
        print("\nBilan annuel du scénario 1:")
        print(bilan)
    elif scenario == 2:
        bilan = scenario_2(GenerateurAlea(IX, IY, IZ))
        print("\nBilan annuel du scénario 2:")
        print(bilan)
    elif scenario == 3:
        bilan_2026, bilan_2030, bilan_2035, bilan_reserve = n_fois_scenario_1(40)
        print("\nBilan de l'année 2026 sur 40 simulations:")
        print(bilan_2026)
        print("\nBilan de l'année 2030 sur 40 simulations:")
        print(bilan_2030)
        print("\nBilan de l'année 2035 sur 40 simulations:")
        print(bilan_2035)
        print("\nÉvolution de la réserve de 2026 à 2035 sur 40 simulations:")
        print(bilan_reserve)
    elif scenario == 4:
        bilan_2026, bilan_2030, bilan_2035, bilan_reserve = n_fois_scenario_2(40)
        print("\nBilan de l'année 2026 sur 40 simulations:")
        print(bilan_2026)
        print("\nBilan de l'année 2030 sur 40 simulations:")
        print(bilan_2030)
        print("\nBilan de l'année 2035 sur 40 simulations:")
        print(bilan_2035)
        print("\nÉvolution de la réserve de 2026 à 2035 sur 40 simulations:")
        print(bilan_reserve)
    else:
        print("Scénario invalide. Veuillez entrer '1' ou '2'.")

if __name__ == "__main__":
    main()