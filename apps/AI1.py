<<<<<<< HEAD
# app.py

import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
def run():
    st.title("🛣️ Assistant IA - Évaluation Environnementale Autoroutière")

    class ImpactEnvironnemental:
        """Classe représentant un impact environnemental avec ses mesures d'atténuation"""
        
        def __init__(self, nom: str, description: str, nature: str, mesures: List[str], periode: str = ""):
            self.nom = nom
            self.description = description
            self.nature = nature  # Positif, Négatif, Risque
            self.mesures = mesures
            self.periode = periode
        
        def to_dict(self) -> Dict:
            return {
                "nom": self.nom,
                "description": self.description,
                "nature": self.nature,
                "mesures": self.mesures,
                "periode": self.periode
            }

    class ComposanteEnvironnementale:
        """Classe représentant une composante environnementale (Air, Eau, Sol, etc.)"""
        
        def __init__(self, nom: str, milieu: str, impacts: List[ImpactEnvironnemental]):
            self.nom = nom
            self.milieu = milieu  # PHYSIQUE, BIOLOGIQUE, HUMAIN
            self.impacts = impacts
        
        def get_impacts_par_nature(self, nature: str) -> List[ImpactEnvironnemental]:
            """Retourne les impacts d'une nature donnée (Positif, Négatif, Risque)"""
            return [impact for impact in self.impacts if impact.nature == nature]
        
        def get_impacts_par_periode(self, periode: str) -> List[ImpactEnvironnemental]:
            """Retourne les impacts d'une période donnée (Construction, Exploitation, Démantèlement)"""
            return [impact for impact in self.impacts if periode.lower() in impact.periode.lower()]

    class BaseConnaissancesAutoroutiere:
        """Base de connaissances spécialisée pour les projets autoroutiers"""
        
        def __init__(self):
            self.composantes = self._initialiser_base_connaissances()
            self.mots_cles = self._initialiser_mots_cles()
        
        def _initialiser_mots_cles(self) -> Dict[str, List[str]]:
            """Initialise les mots-clés pour la détection des thématiques"""
            return {
                "air": ["air", "poussière", "émission", "gaz", "co2", "odeur", "volatil", "pollution atmosphérique", "particules"],
                "eau": ["eau", "nappe", "oued", "cours d'eau", "ruissellement", "assainissement", "pollution hydrique", "hydrocarbure"],
                "sol": ["sol", "terrain", "topographie", "terrassement", "érosion", "contamination", "déblai", "remblai"],
                "bruit": ["bruit", "sonore", "vibration", "nuisance", "décibel", "acoustique"],
                "faune_flore": ["faune", "flore", "biodiversité", "habitat", "écosystème", "espèce", "végétation"],
                "paysage": ["paysage", "visuel", "esthétique", "intégration paysagère"],
                "construction": ["construction", "chantier", "travaux", "terrassement", "défrichement"],
                "exploitation": ["exploitation", "trafic", "circulation", "maintenance", "entretien"],
                "démantèlement": ["démantèlement", "démolition", "remise en état"]
            }
        
        def _initialiser_base_connaissances(self) -> Dict[str, ComposanteEnvironnementale]:
            """Initialise la base de connaissances basée sur les bonnes pratiques autoroutières"""
            
            # === MILIEU PHYSIQUE ===
            
            # AIR
            air_impacts = [
                ImpactEnvironnemental(
                    "Envols de poussières et émissions",
                    "Envols de poussières lors des travaux, émissions de gaz d'échappement des engins, émissions volatiles, risque d'émanation d'odeurs",
                    "Négatif",
                    [
                        "Arrosage des pistes d'accès et zones remaniées",
                        "Limitation de la vitesse des véhicules de chantier",
                        "Protection des zones de stockage contre l'envol des poussières",
                        "Arrêt des moteurs en stationnement",
                        "Inspection et entretien régulier des véhicules et engins",
                        "Utilisation de carburants appropriés",
                        "Interdiction de brûler des déchets sur le chantier",
                        "Stockage approprié des produits volatils en contenants fermés",
                        "Bonne gestion des déchets avec évacuation vers décharge contrôlée"
                    ],
                    "Construction/Démantèlement"
                ),
                ImpactEnvironnemental(
                    "Dégradation qualité air exploitation",
                    "Émissions de CO2 des véhicules, aux péages et aires de service, lors des entretiens, émanations d'odeurs",
                    "Risque",
                    [
                        "Fluidifier le trafic et réduire les durées d'attente aux péages",
                        "Réduire et planifier les délais d'interventions d'entretien",
                        "Inspections visuelles du réseau d'assainissement",
                        "Respect du plan de gestion des déchets",
                        "Interdiction de brûlage ou dépôt sauvage aux aires de service",
                        "Promotion des véhicules électriques aux aires"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Réduction émissions GES",
                    "Décongestion du réseau routier existant et réduction des émissions de GES",
                    "Positif",
                    [
                        "Conception optimisée pour fluidifier le trafic",
                        "Réduction des temps de parcours",
                        "Diminution de la consommation de carburant"
                    ],
                    "Exploitation"
                )
            ]
            
            # EAU
            eau_impacts = [
                ImpactEnvironnemental(
                    "Imperméabilisation et contamination",
                    "Risque d'imperméabilisation, contamination par ruissellement d'eaux usées, rejets accidentels d'hydrocarbures",
                    "Risque",
                    [
                        "Mise en place d'un système de drainage pour éviter stagnation",
                        "Installations de chantier éloignées des cours d'eau (>10m)",
                        "Aucun rejet liquide ou solide dans le réseau hydrographique",
                        "Eaux usées acheminées vers latrines vidangeables",
                        "Entretien régulier des véhicules et engins",
                        "Opérations d'entretien réalisées hors chantier",
                        "Parc de stationnement sur plateforme étanche avec déshuileur",
                        "Kit de dépollution pour gestion de fuite accidentelle",
                        "Stockage matières dangereuses avec dispositifs de rétention",
                        "Interdiction stockage produits dangereux près des cours d'eau",
                        "Plan de dépollution en cas de pollution accidentelle"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Contamination en exploitation",
                    "Contamination suite à rupture canalisation, dysfonctionnement assainissement, incidents technologiques",
                    "Risque",
                    [
                        "Entretien des déshuileurs au niveau des ouvrages d'art et aires",
                        "Entretien des stations d'épuration compactes",
                        "Traitement eaux usées conforme à la réglementation",
                        "Contrôles réguliers qualité des eaux",
                        "Interdiction rejet dans les cours d'eau",
                        "Kits d'intervention d'urgence aux points critiques",
                        "Bonne gestion des déchets"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Amélioration gestion eaux pluviales",
                    "Meilleure collecte et traitement des eaux de ruissellement",
                    "Positif",
                    [
                        "Système d'assainissement intégré",
                        "Bassins de rétention dimensionnés",
                        "Dispositifs de traitement avant rejet"
                    ],
                    "Exploitation"
                )
            ]
            
            # SOL
            sol_impacts = [
                ImpactEnvironnemental(
                    "Pollution et instabilité des sols",
                    "Pollution chimique accidentelle, accumulation de déchets, déblaiement de sols contaminés, instabilité par éboulement",
                    "Risque",
                    [
                        "Organisation du chantier (entretien engins, gestion matériaux)",
                        "Dépôt des déblais en décharge contrôlée",
                        "Réutilisation des matériaux de déblais en remblais",
                        "Zones de stockage dédiées par type de déchet",
                        "Évacuation régulière par entreprises autorisées",
                        "Procédure d'intervention en cas de pollution historique",
                        "Précautions contre fuites et déversements accidentels"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Valorisation des matériaux",
                    "Réutilisation optimale des matériaux excavés et réduction des apports extérieurs",
                    "Positif",
                    [
                        "Étude géotechnique préalable",
                        "Plan de mouvement des terres optimisé",
                        "Réemploi maximum des matériaux sur site"
                    ],
                    "Construction"
                )
            ]
            
            # TOPOGRAPHIE
            topographie_impacts = [
                ImpactEnvironnemental(
                    "Modification topographique",
                    "Modification du terrain par terrassement, accumulation de déblais, modification des cours d'eau",
                    "Négatif",
                    [
                        "Plan de mouvement des terres (bilan déblais/remblais)",
                        "Limiter les zones d'emprunt et de terrassement",
                        "Dispositifs anti-transport de sédiments vers cours d'eau",
                        "Limitation des zones de travaux au niveau des cours d'eau",
                        "Interdiction stockage matériaux dans le lit des cours d'eau",
                        "Système de drainage pour bon écoulement des eaux",
                        "Modélisation des écoulements hydrauliques"
                    ],
                    "Construction/Exploitation"
                )
            ]
            
            # === MILIEU BIOLOGIQUE ===
            
            faune_flore_impacts = [
                ImpactEnvironnemental(
                    "Perte d'habitat et nuisances faune",
                    "Perte d'habitat lors du décapage, nuisances par poussières, bruit et vibrations",
                    "Négatif",
                    [
                        "Minimiser le périmètre d'intervention et décapage",
                        "Stockage et réutilisation terre végétale pour espaces verts",
                        "Protection des arbres et arbustes existants",
                        "Interdiction prélèvement flore locale ou chasse faune",
                        "Cordon de sécurité si espèces protégées identifiées",
                        "Calendrier des travaux adapté aux cycles biologiques",
                        "Passages à faune si nécessaire"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Fragmentation des habitats",
                    "Effet de coupure de l'infrastructure sur les déplacements de la faune",
                    "Négatif",
                    [
                        "Ouvrages de franchissement pour la faune",
                        "Clôtures directionnelles vers les passages",
                        "Maintien de corridors écologiques",
                        "Végétalisation des talus avec espèces locales"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Amélioration habitats compensatoires",
                    "Création de nouveaux habitats et espaces verts",
                    "Positif",
                    [
                        "Plantations d'espèces indigènes",
                        "Création de zones humides compensatoires",
                        "Gestion écologique des dépendances vertes"
                    ],
                    "Construction/Exploitation"
                )
            ]
            
            # === MILIEU HUMAIN ===
            
            bruit_impacts = [
                ImpactEnvironnemental(
                    "Nuisances sonores chantier",
                    "Perturbations sonores dues aux travaux et circulation d'engins",
                    "Négatif",
                    [
                        "Planning définissant durée des travaux",
                        "Emploi d'engins silencieux",
                        "Réglage niveau sonore des avertisseurs",
                        "Arrêt moteurs en stationnement",
                        "Respect horaires de travail (7h-18h en semaine)",
                        "Limitation à 85 dB(A) pour locaux techniques",
                        "Écrans acoustiques temporaires si nécessaire"
                    ],
                    "Construction/Démantèlement"
                ),
                ImpactEnvironnemental(
                    "Nuisances trafic exploitation",
                    "Nuisances sonores dues au trafic autoroutier près des habitations",
                    "Négatif",
                    [
                        "Barrières antibruit aux zones sensibles",
                        "Revêtement routier absorbant",
                        "Optimisation du tracé pour éloigner des habitations",
                        "Merlons paysagers"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Réduction nuisances globales",
                    "Diminution du bruit sur le réseau existant par report de trafic",
                    "Positif",
                    [
                        "Délestage du trafic des voies urbaines",
                        "Réduction des embouteillages sources de bruit"
                    ],
                    "Exploitation"
                )
            ]
            
            qualite_vie_impacts = [
                ImpactEnvironnemental(
                    "Perturbations temporaires",
                    "Perturbation circulation, augmentation bruit et poussières, perturbation des usages locaux",
                    "Négatif",
                    [
                        "Plan de circulation et signalisation",
                        "Arrosage régulier des pistes d'accès",
                        "Programme de communication vers population locale",
                        "Clôture chantier maintenue en bon état",
                        "Respect obligations de signalisation",
                        "Passerelles pour maintien accès piétonnier",
                        "Balisage et panneaux de signalisation temporaire",
                        "Coordination avec services d'urgence"
                    ],
                    "Construction/Démantèlement"
                ),
                ImpactEnvironnemental(
                    "Amélioration cadre de vie",
                    "Amélioration de la liaison routière, fluidité et sécurité du trafic",
                    "Positif",
                    [
                        "Conception pour sécurité et fluidité",
                        "Réduction des temps de parcours",
                        "Diminution des risques d'accidents",
                        "Intégration paysagère soignée"
                    ],
                    "Exploitation"
                )
            ]
            
            economie_impacts = [
                ImpactEnvironnemental(
                    "Impact économique construction",
                    "Emplois temporaires, retombées économiques locales, nuisances commerciales",
                    "Positif",
                    [
                        "Privilégier la main d'œuvre locale",
                        "Sous-traitance avec entreprises régionales",
                        "Maintien accès aux commerces durant travaux",
                        "Communication sur planning des travaux"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Développement économique",
                    "Amélioration de l'accessibilité, développement économique régional",
                    "Positif",
                    [
                        "Facilitation des échanges économiques",
                        "Désenclavement de certaines zones",
                        "Attraction d'investissements"
                    ],
                    "Exploitation"
                )
            ]
            
            return {
                "air": ComposanteEnvironnementale("Air", "PHYSIQUE", air_impacts),
                "eau": ComposanteEnvironnementale("Eau de surface et souterraine", "PHYSIQUE", eau_impacts),
                "sol": ComposanteEnvironnementale("Sols", "PHYSIQUE", sol_impacts),
                "topographie": ComposanteEnvironnementale("Topographie", "PHYSIQUE", topographie_impacts),
                "faune_flore": ComposanteEnvironnementale("Faune et flore", "BIOLOGIQUE", faune_flore_impacts),
                "bruit": ComposanteEnvironnementale("Environnement sonore et vibrations", "HUMAIN", bruit_impacts),
                "qualite_vie": ComposanteEnvironnementale("Qualité de vie et santé", "HUMAIN", qualite_vie_impacts),
                "economie": ComposanteEnvironnementale("Aspects socio-économiques", "HUMAIN", economie_impacts)
            }
        
        def detecter_thematiques(self, texte: str) -> List[str]:
            """Détecte les thématiques environnementales dans le texte"""
            texte_lower = texte.lower()
            thematiques_detectees = []
            
            for thematique, mots_cles in self.mots_cles.items():
                for mot_cle in mots_cles:
                    if mot_cle in texte_lower:
                        if thematique not in thematiques_detectees:
                            thematiques_detectees.append(thematique)
                        break
            
            return thematiques_detectees
        
        def detecter_periode(self, texte: str) -> List[str]:
            """Détecte la période du projet (construction, exploitation, démantèlement)"""
            texte_lower = texte.lower()
            periodes = []
            
            if any(mot in texte_lower for mot in ["construction", "chantier", "travaux", "terrassement"]):
                periodes.append("Construction")
            if any(mot in texte_lower for mot in ["exploitation", "fonctionnement", "circulation", "trafic"]):
                periodes.append("Exploitation")
            if any(mot in texte_lower for mot in ["démantèlement", "démolition", "remise en état"]):
                periodes.append("Démantèlement")
            
            return periodes if periodes else ["Construction", "Exploitation"]
        
        def get_composante(self, nom: str) -> Optional[ComposanteEnvironnementale]:
            """Retourne une composante par son nom"""
            return self.composantes.get(nom)

    class ConversationManager:
        """Gestionnaire de l'historique des conversations"""
        
        def __init__(self):
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = []
        
        def ajouter_message(self, type_msg: str, contenu: str, timestamp: datetime = None):
            """Ajoute un message à l'historique"""
            if timestamp is None:
                timestamp = datetime.now()
            
            st.session_state.conversation_history.append({
                'type': type_msg,
                'contenu': contenu,
                'timestamp': timestamp
            })
        
        def get_historique(self) -> List[Dict]:
            """Retourne l'historique des conversations"""
            return st.session_state.conversation_history
        
        def effacer_historique(self):
            """Efface l'historique des conversations"""
            st.session_state.conversation_history = []

    class ChatbotAutoroutier:
        """Chatbot spécialisé pour l'évaluation environnementale autoroutière"""
        
        def __init__(self):
            self.base_connaissances = BaseConnaissancesAutoroutiere()
            self.conversation_manager = ConversationManager()
        
        def analyser_demande(self, texte_utilisateur: str) -> str:
            """Analyse la demande utilisateur et génère une réponse spécialisée"""
            thematiques_detectees = self.base_connaissances.detecter_thematiques(texte_utilisateur)
            periodes_detectees = self.base_connaissances.detecter_periode(texte_utilisateur)
            
            if not thematiques_detectees:
                return self._generer_reponse_aide()
            
            return self._generer_analyse_complete(thematiques_detectees, periodes_detectees, texte_utilisateur)
        
        def _generer_reponse_aide(self) -> str:
            """Génère une réponse d'aide quand aucune thématique n'est détectée"""
            return """🤔 **Je n'ai pas identifié de thématiques environnementales spécifiques dans votre message.**

    📋 **Thématiques que je peux analyser pour les projets autoroutiers :**
    • **Air** : pollution, poussières, émissions, odeurs
    • **Eau** : contamination, ruissellement, assainissement, cours d'eau
    • **Sol** : pollution, érosion, stabilité, terrassement
    • **Bruit** : nuisances sonores, vibrations
    • **Biodiversité** : faune, flore, habitats, écosystèmes
    • **Paysage** : intégration visuelle, impact esthétique
    • **Social** : qualité de vie, économie locale

    🏗️ **Phases de projet autoroutier :**
    • **Construction** : chantier, travaux, terrassement
    • **Exploitation** : circulation, trafic, maintenance
    • **Démantèlement** : démolition, remise en état

    💡 **Exemple de question :** *"Quels sont les impacts sur l'air et l'eau pendant la phase de construction de notre projet autoroutier ?"*"""
        
        def _generer_analyse_complete(self, thematiques: List[str], periodes: List[str], texte_original: str) -> str:
            """Génère une analyse environnementale complète"""
            reponse = f"🎯 **Analyse Environnementale - Projet Autoroutier**\n\n"
            reponse += f"📊 **Synthèse détectée :**\n"
            reponse += f"• **{len(thematiques)} thématique(s) environnementale(s)** identifiée(s)\n"
            reponse += f"• **Phase(s) concernée(s) :** {', '.join(periodes)}\n\n"
            
            impacts_totaux = 0
            mesures_totales = 0
            
            for thematique in thematiques:
                composante = self.base_connaissances.get_composante(thematique)
                if not composante:
                    continue
                
                reponse += f"## 🌍 **{composante.nom.upper()}** *(Milieu {composante.milieu})*\n\n"
                
                impacts_pertinents = []
                for periode in periodes:
                    impacts_periode = composante.get_impacts_par_periode(periode)
                    impacts_pertinents.extend(impacts_periode)
                
                # Éliminer les doublons
                impacts_uniques = []
                noms_impacts = set()
                for impact in impacts_pertinents:
                    if impact.nom not in noms_impacts:
                        impacts_uniques.append(impact)
                        noms_impacts.add(impact.nom)
                
                if not impacts_uniques:
                    impacts_uniques = composante.impacts
                
                for impact in impacts_uniques:
                    impacts_totaux += 1
                    mesures_totales += len(impact.mesures)
                    
                    # Icône selon la nature de l'impact
                    icone = "⚠️" if impact.nature == "Risque" else ("❌" if impact.nature == "Négatif" else "✅")
                    
                    reponse += f"### {icone} **{impact.nom}** *({impact.nature})*\n"
                    reponse += f"📝 *{impact.description}*\n\n"
                    
                    if impact.mesures:
                        reponse += f"**🛡️ Mesures d'atténuation/compensation ({len(impact.mesures)}) :**\n"
                        for i, mesure in enumerate(impact.mesures, 1):
                            reponse += f"{i}. {mesure}\n"
                        reponse += "\n"
                
                reponse += "─" * 60 + "\n\n"
            
            # Résumé final
            reponse += f"📈 **Bilan de l'analyse :**\n"
            reponse += f"• **{impacts_totaux} impacts** environnementaux identifiés\n"
            reponse += f"• **{mesures_totales} mesures** d'atténuation proposées\n"
            reponse += f"• **Priorité :** Intégrer ces mesures dès la conception du projet\n\n"
            
            reponse += "💼 **Recommandation :** Ces analyses sont basées sur les meilleures pratiques "
            reponse += "des projets autoroutiers. Adaptez les mesures selon les spécificités de votre site et les réglementations locales."
            
            return reponse
        
        def traiter_conversation(self, message_utilisateur: str):
            """Traite un message utilisateur et met à jour la conversation"""
            self.conversation_manager.ajouter_message("user", message_utilisateur)
            reponse_ia = self.analyser_demande(message_utilisateur)
            self.conversation_manager.ajouter_message("assistant", reponse_ia)

    def main():
        """Fonction principale de l'application Streamlit"""
        
        
        # Initialisation
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = ChatbotAutoroutier()
        
        chatbot = st.session_state.chatbot
        
        # Interface utilisateur
        st.markdown("*Spécialisé dans l'analyse des impacts environnementaux des projets autoroutiers*")
        
        # Sidebar with updated guide
        with st.sidebar:
            st.header("🎯 Assistant IA Environnemental")
            
            # Quick stats
            st.info("""
            **📊 Capacités d'analyse :**
            - **8 domaines** environnementaux
            - **3 phases** de projet
            - **20+ impacts** identifiables
            - **100+ mesures** préventives
            """)
            
            # Interactive examples
            st.subheader("💡 Exemples de questions")
            
            example_questions = [
                "Impact du terrassement sur l'eau et les sols",
                "Nuisances sonores pendant la construction",
                "Mesures pour protéger la biodiversité",
                "Pollution de l'air en phase d'exploitation",
                "Aspects économiques et sociaux du projet"
            ]
            
            selected_example = st.selectbox(
                "Sélectionnez un exemple :",
                ["Choisir un exemple..."] + example_questions
            )
            
            if selected_example != "Choisir un exemple...":
                if st.button("🚀 Utiliser cet exemple", use_container_width=True):
                    st.session_state.example_input = selected_example
                    st.rerun()
            
            st.markdown("---")
            
            # Quick tips
            st.subheader("💡 Conseils d'utilisation")
            with st.expander("🔍 Comment bien formuler votre question"):
                st.markdown("""
                **Pour une analyse optimale :**
                
                ✅ **Précisez la phase** : construction, exploitation, démantèlement
                
                ✅ **Mentionnez les domaines** : air, eau, sol, bruit, faune, etc.
                
                ✅ **Décrivez le contexte** : type de terrain, proximité d'habitations, cours d'eau...
                
                **Exemple optimal :**
                *"Notre projet autoroutier traverse une zone forestière avec un cours d'eau. Quels impacts sur la faune et l'eau pendant la construction ?"*
                """)
            
            with st.expander("📋 Domaines d'expertise"):
                st.markdown("""
                **🌍 Milieu physique :**
                - Qualité de l'air et émissions
                - Ressources en eau
                - Sols et géologie
                - Topographie et drainage
                
                **🌿 Milieu biologique :**
                - Faune et habitats
                - Flore et écosystèmes
                - Corridors écologiques
                
                **👥 Milieu humain :**
                - Environnement sonore
                - Qualité de vie
                - Développement économique
                - Paysage et patrimoine
                """)
            
            st.markdown("---")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Nouvelle\nconversation", use_container_width=True):
                    chatbot.conversation_manager.effacer_historique()
                    st.rerun()
            
            with col2:
                if st.button("📊 Statistiques\nde session", use_container_width=True):
                    historique = chatbot.conversation_manager.get_historique()
                    user_messages = [msg for msg in historique if msg['type'] == 'user']
                    st.success(f"**{len(user_messages)}** questions posées")
            
            # Footer info
            st.markdown("---")
            st.caption("🤖 Assistant IA spécialisé en évaluation environnementale autoroutière")
        
        
        # Zone de conversation
        st.markdown("### 💬 Conversation")
        
        # Container pour l'historique avec hauteur fixe
        chat_container = st.container()
        
        with chat_container:
            historique = chatbot.conversation_manager.get_historique()
            
            if not historique:
                st.info("👋 **Bonjour !** Je suis votre assistant IA spécialisé en évaluation environnementale autoroutière. Décrivez-moi votre projet et je vous fournirai une analyse détaillée des impacts et mesures d'atténuation.")
            
            for msg in historique:
                timestamp_str = msg['timestamp'].strftime("%H:%M:%S")
                
                if msg['type'] == 'user':
                    with st.chat_message("user"):
                        st.write(f"**{timestamp_str}** - {msg['contenu']}")
                else:
                    with st.chat_message("assistant"):
                        st.write(f"**{timestamp_str}**")
                        st.markdown(msg['contenu'])
        
        # Zone de saisie
        st.markdown("### ✍️ Votre question")
        
        with st.form(key="message_form", clear_on_submit=True):
            user_input = st.text_area(
                "Décrivez votre projet autoroutier :",
                height=120,
                placeholder="Exemple : Nous planifions la construction d'une nouvelle section autoroutière avec terrassement important, traversée de cours d'eau et circulation intense d'engins. Quels sont les principaux impacts sur l'eau et l'air ?",
                key="user_input"
            )
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                submitted = st.form_submit_button(
                    "🚀 Analyser", 
                    use_container_width=True,
                    type="primary"
                )
        
        # Traitement du message
        if submitted and user_input.strip():
            with st.spinner("🔍 Analyse environnementale en cours..."):
                chatbot.traiter_conversation(user_input.strip())
            st.rerun()
        elif submitted and not user_input.strip():
            st.warning("⚠️ Veuillez décrire votre projet avant de lancer l'analyse.")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "*Assistant IA basé sur les meilleures pratiques d'évaluation environnementale autoroutière*",
            help="Cet outil utilise une base de connaissances spécialisée pour fournir des analyses personnalisées selon votre projet."
        )

    main()
if __name__ == "__main__":
=======
# app.py

import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
def run():
    st.title("🛣️ Assistant IA - Évaluation Environnementale Autoroutière")

    class ImpactEnvironnemental:
        """Classe représentant un impact environnemental avec ses mesures d'atténuation"""
        
        def __init__(self, nom: str, description: str, nature: str, mesures: List[str], periode: str = ""):
            self.nom = nom
            self.description = description
            self.nature = nature  # Positif, Négatif, Risque
            self.mesures = mesures
            self.periode = periode
        
        def to_dict(self) -> Dict:
            return {
                "nom": self.nom,
                "description": self.description,
                "nature": self.nature,
                "mesures": self.mesures,
                "periode": self.periode
            }

    class ComposanteEnvironnementale:
        """Classe représentant une composante environnementale (Air, Eau, Sol, etc.)"""
        
        def __init__(self, nom: str, milieu: str, impacts: List[ImpactEnvironnemental]):
            self.nom = nom
            self.milieu = milieu  # PHYSIQUE, BIOLOGIQUE, HUMAIN
            self.impacts = impacts
        
        def get_impacts_par_nature(self, nature: str) -> List[ImpactEnvironnemental]:
            """Retourne les impacts d'une nature donnée (Positif, Négatif, Risque)"""
            return [impact for impact in self.impacts if impact.nature == nature]
        
        def get_impacts_par_periode(self, periode: str) -> List[ImpactEnvironnemental]:
            """Retourne les impacts d'une période donnée (Construction, Exploitation, Démantèlement)"""
            return [impact for impact in self.impacts if periode.lower() in impact.periode.lower()]

    class BaseConnaissancesAutoroutiere:
        """Base de connaissances spécialisée pour les projets autoroutiers"""
        
        def __init__(self):
            self.composantes = self._initialiser_base_connaissances()
            self.mots_cles = self._initialiser_mots_cles()
        
        def _initialiser_mots_cles(self) -> Dict[str, List[str]]:
            """Initialise les mots-clés pour la détection des thématiques"""
            return {
                "air": ["air", "poussière", "émission", "gaz", "co2", "odeur", "volatil", "pollution atmosphérique", "particules"],
                "eau": ["eau", "nappe", "oued", "cours d'eau", "ruissellement", "assainissement", "pollution hydrique", "hydrocarbure"],
                "sol": ["sol", "terrain", "topographie", "terrassement", "érosion", "contamination", "déblai", "remblai"],
                "bruit": ["bruit", "sonore", "vibration", "nuisance", "décibel", "acoustique"],
                "faune_flore": ["faune", "flore", "biodiversité", "habitat", "écosystème", "espèce", "végétation"],
                "paysage": ["paysage", "visuel", "esthétique", "intégration paysagère"],
                "construction": ["construction", "chantier", "travaux", "terrassement", "défrichement"],
                "exploitation": ["exploitation", "trafic", "circulation", "maintenance", "entretien"],
                "démantèlement": ["démantèlement", "démolition", "remise en état"]
            }
        
        def _initialiser_base_connaissances(self) -> Dict[str, ComposanteEnvironnementale]:
            """Initialise la base de connaissances basée sur les bonnes pratiques autoroutières"""
            
            # === MILIEU PHYSIQUE ===
            
            # AIR
            air_impacts = [
                ImpactEnvironnemental(
                    "Envols de poussières et émissions",
                    "Envols de poussières lors des travaux, émissions de gaz d'échappement des engins, émissions volatiles, risque d'émanation d'odeurs",
                    "Négatif",
                    [
                        "Arrosage des pistes d'accès et zones remaniées",
                        "Limitation de la vitesse des véhicules de chantier",
                        "Protection des zones de stockage contre l'envol des poussières",
                        "Arrêt des moteurs en stationnement",
                        "Inspection et entretien régulier des véhicules et engins",
                        "Utilisation de carburants appropriés",
                        "Interdiction de brûler des déchets sur le chantier",
                        "Stockage approprié des produits volatils en contenants fermés",
                        "Bonne gestion des déchets avec évacuation vers décharge contrôlée"
                    ],
                    "Construction/Démantèlement"
                ),
                ImpactEnvironnemental(
                    "Dégradation qualité air exploitation",
                    "Émissions de CO2 des véhicules, aux péages et aires de service, lors des entretiens, émanations d'odeurs",
                    "Risque",
                    [
                        "Fluidifier le trafic et réduire les durées d'attente aux péages",
                        "Réduire et planifier les délais d'interventions d'entretien",
                        "Inspections visuelles du réseau d'assainissement",
                        "Respect du plan de gestion des déchets",
                        "Interdiction de brûlage ou dépôt sauvage aux aires de service",
                        "Promotion des véhicules électriques aux aires"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Réduction émissions GES",
                    "Décongestion du réseau routier existant et réduction des émissions de GES",
                    "Positif",
                    [
                        "Conception optimisée pour fluidifier le trafic",
                        "Réduction des temps de parcours",
                        "Diminution de la consommation de carburant"
                    ],
                    "Exploitation"
                )
            ]
            
            # EAU
            eau_impacts = [
                ImpactEnvironnemental(
                    "Imperméabilisation et contamination",
                    "Risque d'imperméabilisation, contamination par ruissellement d'eaux usées, rejets accidentels d'hydrocarbures",
                    "Risque",
                    [
                        "Mise en place d'un système de drainage pour éviter stagnation",
                        "Installations de chantier éloignées des cours d'eau (>10m)",
                        "Aucun rejet liquide ou solide dans le réseau hydrographique",
                        "Eaux usées acheminées vers latrines vidangeables",
                        "Entretien régulier des véhicules et engins",
                        "Opérations d'entretien réalisées hors chantier",
                        "Parc de stationnement sur plateforme étanche avec déshuileur",
                        "Kit de dépollution pour gestion de fuite accidentelle",
                        "Stockage matières dangereuses avec dispositifs de rétention",
                        "Interdiction stockage produits dangereux près des cours d'eau",
                        "Plan de dépollution en cas de pollution accidentelle"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Contamination en exploitation",
                    "Contamination suite à rupture canalisation, dysfonctionnement assainissement, incidents technologiques",
                    "Risque",
                    [
                        "Entretien des déshuileurs au niveau des ouvrages d'art et aires",
                        "Entretien des stations d'épuration compactes",
                        "Traitement eaux usées conforme à la réglementation",
                        "Contrôles réguliers qualité des eaux",
                        "Interdiction rejet dans les cours d'eau",
                        "Kits d'intervention d'urgence aux points critiques",
                        "Bonne gestion des déchets"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Amélioration gestion eaux pluviales",
                    "Meilleure collecte et traitement des eaux de ruissellement",
                    "Positif",
                    [
                        "Système d'assainissement intégré",
                        "Bassins de rétention dimensionnés",
                        "Dispositifs de traitement avant rejet"
                    ],
                    "Exploitation"
                )
            ]
            
            # SOL
            sol_impacts = [
                ImpactEnvironnemental(
                    "Pollution et instabilité des sols",
                    "Pollution chimique accidentelle, accumulation de déchets, déblaiement de sols contaminés, instabilité par éboulement",
                    "Risque",
                    [
                        "Organisation du chantier (entretien engins, gestion matériaux)",
                        "Dépôt des déblais en décharge contrôlée",
                        "Réutilisation des matériaux de déblais en remblais",
                        "Zones de stockage dédiées par type de déchet",
                        "Évacuation régulière par entreprises autorisées",
                        "Procédure d'intervention en cas de pollution historique",
                        "Précautions contre fuites et déversements accidentels"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Valorisation des matériaux",
                    "Réutilisation optimale des matériaux excavés et réduction des apports extérieurs",
                    "Positif",
                    [
                        "Étude géotechnique préalable",
                        "Plan de mouvement des terres optimisé",
                        "Réemploi maximum des matériaux sur site"
                    ],
                    "Construction"
                )
            ]
            
            # TOPOGRAPHIE
            topographie_impacts = [
                ImpactEnvironnemental(
                    "Modification topographique",
                    "Modification du terrain par terrassement, accumulation de déblais, modification des cours d'eau",
                    "Négatif",
                    [
                        "Plan de mouvement des terres (bilan déblais/remblais)",
                        "Limiter les zones d'emprunt et de terrassement",
                        "Dispositifs anti-transport de sédiments vers cours d'eau",
                        "Limitation des zones de travaux au niveau des cours d'eau",
                        "Interdiction stockage matériaux dans le lit des cours d'eau",
                        "Système de drainage pour bon écoulement des eaux",
                        "Modélisation des écoulements hydrauliques"
                    ],
                    "Construction/Exploitation"
                )
            ]
            
            # === MILIEU BIOLOGIQUE ===
            
            faune_flore_impacts = [
                ImpactEnvironnemental(
                    "Perte d'habitat et nuisances faune",
                    "Perte d'habitat lors du décapage, nuisances par poussières, bruit et vibrations",
                    "Négatif",
                    [
                        "Minimiser le périmètre d'intervention et décapage",
                        "Stockage et réutilisation terre végétale pour espaces verts",
                        "Protection des arbres et arbustes existants",
                        "Interdiction prélèvement flore locale ou chasse faune",
                        "Cordon de sécurité si espèces protégées identifiées",
                        "Calendrier des travaux adapté aux cycles biologiques",
                        "Passages à faune si nécessaire"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Fragmentation des habitats",
                    "Effet de coupure de l'infrastructure sur les déplacements de la faune",
                    "Négatif",
                    [
                        "Ouvrages de franchissement pour la faune",
                        "Clôtures directionnelles vers les passages",
                        "Maintien de corridors écologiques",
                        "Végétalisation des talus avec espèces locales"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Amélioration habitats compensatoires",
                    "Création de nouveaux habitats et espaces verts",
                    "Positif",
                    [
                        "Plantations d'espèces indigènes",
                        "Création de zones humides compensatoires",
                        "Gestion écologique des dépendances vertes"
                    ],
                    "Construction/Exploitation"
                )
            ]
            
            # === MILIEU HUMAIN ===
            
            bruit_impacts = [
                ImpactEnvironnemental(
                    "Nuisances sonores chantier",
                    "Perturbations sonores dues aux travaux et circulation d'engins",
                    "Négatif",
                    [
                        "Planning définissant durée des travaux",
                        "Emploi d'engins silencieux",
                        "Réglage niveau sonore des avertisseurs",
                        "Arrêt moteurs en stationnement",
                        "Respect horaires de travail (7h-18h en semaine)",
                        "Limitation à 85 dB(A) pour locaux techniques",
                        "Écrans acoustiques temporaires si nécessaire"
                    ],
                    "Construction/Démantèlement"
                ),
                ImpactEnvironnemental(
                    "Nuisances trafic exploitation",
                    "Nuisances sonores dues au trafic autoroutier près des habitations",
                    "Négatif",
                    [
                        "Barrières antibruit aux zones sensibles",
                        "Revêtement routier absorbant",
                        "Optimisation du tracé pour éloigner des habitations",
                        "Merlons paysagers"
                    ],
                    "Exploitation"
                ),
                ImpactEnvironnemental(
                    "Réduction nuisances globales",
                    "Diminution du bruit sur le réseau existant par report de trafic",
                    "Positif",
                    [
                        "Délestage du trafic des voies urbaines",
                        "Réduction des embouteillages sources de bruit"
                    ],
                    "Exploitation"
                )
            ]
            
            qualite_vie_impacts = [
                ImpactEnvironnemental(
                    "Perturbations temporaires",
                    "Perturbation circulation, augmentation bruit et poussières, perturbation des usages locaux",
                    "Négatif",
                    [
                        "Plan de circulation et signalisation",
                        "Arrosage régulier des pistes d'accès",
                        "Programme de communication vers population locale",
                        "Clôture chantier maintenue en bon état",
                        "Respect obligations de signalisation",
                        "Passerelles pour maintien accès piétonnier",
                        "Balisage et panneaux de signalisation temporaire",
                        "Coordination avec services d'urgence"
                    ],
                    "Construction/Démantèlement"
                ),
                ImpactEnvironnemental(
                    "Amélioration cadre de vie",
                    "Amélioration de la liaison routière, fluidité et sécurité du trafic",
                    "Positif",
                    [
                        "Conception pour sécurité et fluidité",
                        "Réduction des temps de parcours",
                        "Diminution des risques d'accidents",
                        "Intégration paysagère soignée"
                    ],
                    "Exploitation"
                )
            ]
            
            economie_impacts = [
                ImpactEnvironnemental(
                    "Impact économique construction",
                    "Emplois temporaires, retombées économiques locales, nuisances commerciales",
                    "Positif",
                    [
                        "Privilégier la main d'œuvre locale",
                        "Sous-traitance avec entreprises régionales",
                        "Maintien accès aux commerces durant travaux",
                        "Communication sur planning des travaux"
                    ],
                    "Construction"
                ),
                ImpactEnvironnemental(
                    "Développement économique",
                    "Amélioration de l'accessibilité, développement économique régional",
                    "Positif",
                    [
                        "Facilitation des échanges économiques",
                        "Désenclavement de certaines zones",
                        "Attraction d'investissements"
                    ],
                    "Exploitation"
                )
            ]
            
            return {
                "air": ComposanteEnvironnementale("Air", "PHYSIQUE", air_impacts),
                "eau": ComposanteEnvironnementale("Eau de surface et souterraine", "PHYSIQUE", eau_impacts),
                "sol": ComposanteEnvironnementale("Sols", "PHYSIQUE", sol_impacts),
                "topographie": ComposanteEnvironnementale("Topographie", "PHYSIQUE", topographie_impacts),
                "faune_flore": ComposanteEnvironnementale("Faune et flore", "BIOLOGIQUE", faune_flore_impacts),
                "bruit": ComposanteEnvironnementale("Environnement sonore et vibrations", "HUMAIN", bruit_impacts),
                "qualite_vie": ComposanteEnvironnementale("Qualité de vie et santé", "HUMAIN", qualite_vie_impacts),
                "economie": ComposanteEnvironnementale("Aspects socio-économiques", "HUMAIN", economie_impacts)
            }
        
        def detecter_thematiques(self, texte: str) -> List[str]:
            """Détecte les thématiques environnementales dans le texte"""
            texte_lower = texte.lower()
            thematiques_detectees = []
            
            for thematique, mots_cles in self.mots_cles.items():
                for mot_cle in mots_cles:
                    if mot_cle in texte_lower:
                        if thematique not in thematiques_detectees:
                            thematiques_detectees.append(thematique)
                        break
            
            return thematiques_detectees
        
        def detecter_periode(self, texte: str) -> List[str]:
            """Détecte la période du projet (construction, exploitation, démantèlement)"""
            texte_lower = texte.lower()
            periodes = []
            
            if any(mot in texte_lower for mot in ["construction", "chantier", "travaux", "terrassement"]):
                periodes.append("Construction")
            if any(mot in texte_lower for mot in ["exploitation", "fonctionnement", "circulation", "trafic"]):
                periodes.append("Exploitation")
            if any(mot in texte_lower for mot in ["démantèlement", "démolition", "remise en état"]):
                periodes.append("Démantèlement")
            
            return periodes if periodes else ["Construction", "Exploitation"]
        
        def get_composante(self, nom: str) -> Optional[ComposanteEnvironnementale]:
            """Retourne une composante par son nom"""
            return self.composantes.get(nom)

    class ConversationManager:
        """Gestionnaire de l'historique des conversations"""
        
        def __init__(self):
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = []
        
        def ajouter_message(self, type_msg: str, contenu: str, timestamp: datetime = None):
            """Ajoute un message à l'historique"""
            if timestamp is None:
                timestamp = datetime.now()
            
            st.session_state.conversation_history.append({
                'type': type_msg,
                'contenu': contenu,
                'timestamp': timestamp
            })
        
        def get_historique(self) -> List[Dict]:
            """Retourne l'historique des conversations"""
            return st.session_state.conversation_history
        
        def effacer_historique(self):
            """Efface l'historique des conversations"""
            st.session_state.conversation_history = []

    class ChatbotAutoroutier:
        """Chatbot spécialisé pour l'évaluation environnementale autoroutière"""
        
        def __init__(self):
            self.base_connaissances = BaseConnaissancesAutoroutiere()
            self.conversation_manager = ConversationManager()
        
        def analyser_demande(self, texte_utilisateur: str) -> str:
            """Analyse la demande utilisateur et génère une réponse spécialisée"""
            thematiques_detectees = self.base_connaissances.detecter_thematiques(texte_utilisateur)
            periodes_detectees = self.base_connaissances.detecter_periode(texte_utilisateur)
            
            if not thematiques_detectees:
                return self._generer_reponse_aide()
            
            return self._generer_analyse_complete(thematiques_detectees, periodes_detectees, texte_utilisateur)
        
        def _generer_reponse_aide(self) -> str:
            """Génère une réponse d'aide quand aucune thématique n'est détectée"""
            return """🤔 **Je n'ai pas identifié de thématiques environnementales spécifiques dans votre message.**

    📋 **Thématiques que je peux analyser pour les projets autoroutiers :**
    • **Air** : pollution, poussières, émissions, odeurs
    • **Eau** : contamination, ruissellement, assainissement, cours d'eau
    • **Sol** : pollution, érosion, stabilité, terrassement
    • **Bruit** : nuisances sonores, vibrations
    • **Biodiversité** : faune, flore, habitats, écosystèmes
    • **Paysage** : intégration visuelle, impact esthétique
    • **Social** : qualité de vie, économie locale

    🏗️ **Phases de projet autoroutier :**
    • **Construction** : chantier, travaux, terrassement
    • **Exploitation** : circulation, trafic, maintenance
    • **Démantèlement** : démolition, remise en état

    💡 **Exemple de question :** *"Quels sont les impacts sur l'air et l'eau pendant la phase de construction de notre projet autoroutier ?"*"""
        
        def _generer_analyse_complete(self, thematiques: List[str], periodes: List[str], texte_original: str) -> str:
            """Génère une analyse environnementale complète"""
            reponse = f"🎯 **Analyse Environnementale - Projet Autoroutier**\n\n"
            reponse += f"📊 **Synthèse détectée :**\n"
            reponse += f"• **{len(thematiques)} thématique(s) environnementale(s)** identifiée(s)\n"
            reponse += f"• **Phase(s) concernée(s) :** {', '.join(periodes)}\n\n"
            
            impacts_totaux = 0
            mesures_totales = 0
            
            for thematique in thematiques:
                composante = self.base_connaissances.get_composante(thematique)
                if not composante:
                    continue
                
                reponse += f"## 🌍 **{composante.nom.upper()}** *(Milieu {composante.milieu})*\n\n"
                
                impacts_pertinents = []
                for periode in periodes:
                    impacts_periode = composante.get_impacts_par_periode(periode)
                    impacts_pertinents.extend(impacts_periode)
                
                # Éliminer les doublons
                impacts_uniques = []
                noms_impacts = set()
                for impact in impacts_pertinents:
                    if impact.nom not in noms_impacts:
                        impacts_uniques.append(impact)
                        noms_impacts.add(impact.nom)
                
                if not impacts_uniques:
                    impacts_uniques = composante.impacts
                
                for impact in impacts_uniques:
                    impacts_totaux += 1
                    mesures_totales += len(impact.mesures)
                    
                    # Icône selon la nature de l'impact
                    icone = "⚠️" if impact.nature == "Risque" else ("❌" if impact.nature == "Négatif" else "✅")
                    
                    reponse += f"### {icone} **{impact.nom}** *({impact.nature})*\n"
                    reponse += f"📝 *{impact.description}*\n\n"
                    
                    if impact.mesures:
                        reponse += f"**🛡️ Mesures d'atténuation/compensation ({len(impact.mesures)}) :**\n"
                        for i, mesure in enumerate(impact.mesures, 1):
                            reponse += f"{i}. {mesure}\n"
                        reponse += "\n"
                
                reponse += "─" * 60 + "\n\n"
            
            # Résumé final
            reponse += f"📈 **Bilan de l'analyse :**\n"
            reponse += f"• **{impacts_totaux} impacts** environnementaux identifiés\n"
            reponse += f"• **{mesures_totales} mesures** d'atténuation proposées\n"
            reponse += f"• **Priorité :** Intégrer ces mesures dès la conception du projet\n\n"
            
            reponse += "💼 **Recommandation :** Ces analyses sont basées sur les meilleures pratiques "
            reponse += "des projets autoroutiers. Adaptez les mesures selon les spécificités de votre site et les réglementations locales."
            
            return reponse
        
        def traiter_conversation(self, message_utilisateur: str):
            """Traite un message utilisateur et met à jour la conversation"""
            self.conversation_manager.ajouter_message("user", message_utilisateur)
            reponse_ia = self.analyser_demande(message_utilisateur)
            self.conversation_manager.ajouter_message("assistant", reponse_ia)

    def main():
        """Fonction principale de l'application Streamlit"""
        
        
        # Initialisation
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = ChatbotAutoroutier()
        
        chatbot = st.session_state.chatbot
        
        # Interface utilisateur
        st.markdown("*Spécialisé dans l'analyse des impacts environnementaux des projets autoroutiers*")
        
        # Sidebar with updated guide
        with st.sidebar:
            st.header("🎯 Assistant IA Environnemental")
            
            # Quick stats
            st.info("""
            **📊 Capacités d'analyse :**
            - **8 domaines** environnementaux
            - **3 phases** de projet
            - **20+ impacts** identifiables
            - **100+ mesures** préventives
            """)
            
            # Interactive examples
            st.subheader("💡 Exemples de questions")
            
            example_questions = [
                "Impact du terrassement sur l'eau et les sols",
                "Nuisances sonores pendant la construction",
                "Mesures pour protéger la biodiversité",
                "Pollution de l'air en phase d'exploitation",
                "Aspects économiques et sociaux du projet"
            ]
            
            selected_example = st.selectbox(
                "Sélectionnez un exemple :",
                ["Choisir un exemple..."] + example_questions
            )
            
            if selected_example != "Choisir un exemple...":
                if st.button("🚀 Utiliser cet exemple", use_container_width=True):
                    st.session_state.example_input = selected_example
                    st.rerun()
            
            st.markdown("---")
            
            # Quick tips
            st.subheader("💡 Conseils d'utilisation")
            with st.expander("🔍 Comment bien formuler votre question"):
                st.markdown("""
                **Pour une analyse optimale :**
                
                ✅ **Précisez la phase** : construction, exploitation, démantèlement
                
                ✅ **Mentionnez les domaines** : air, eau, sol, bruit, faune, etc.
                
                ✅ **Décrivez le contexte** : type de terrain, proximité d'habitations, cours d'eau...
                
                **Exemple optimal :**
                *"Notre projet autoroutier traverse une zone forestière avec un cours d'eau. Quels impacts sur la faune et l'eau pendant la construction ?"*
                """)
            
            with st.expander("📋 Domaines d'expertise"):
                st.markdown("""
                **🌍 Milieu physique :**
                - Qualité de l'air et émissions
                - Ressources en eau
                - Sols et géologie
                - Topographie et drainage
                
                **🌿 Milieu biologique :**
                - Faune et habitats
                - Flore et écosystèmes
                - Corridors écologiques
                
                **👥 Milieu humain :**
                - Environnement sonore
                - Qualité de vie
                - Développement économique
                - Paysage et patrimoine
                """)
            
            st.markdown("---")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Nouvelle\nconversation", use_container_width=True):
                    chatbot.conversation_manager.effacer_historique()
                    st.rerun()
            
            with col2:
                if st.button("📊 Statistiques\nde session", use_container_width=True):
                    historique = chatbot.conversation_manager.get_historique()
                    user_messages = [msg for msg in historique if msg['type'] == 'user']
                    st.success(f"**{len(user_messages)}** questions posées")
            
            # Footer info
            st.markdown("---")
            st.caption("🤖 Assistant IA spécialisé en évaluation environnementale autoroutière")
        
        
        # Zone de conversation
        st.markdown("### 💬 Conversation")
        
        # Container pour l'historique avec hauteur fixe
        chat_container = st.container()
        
        with chat_container:
            historique = chatbot.conversation_manager.get_historique()
            
            if not historique:
                st.info("👋 **Bonjour !** Je suis votre assistant IA spécialisé en évaluation environnementale autoroutière. Décrivez-moi votre projet et je vous fournirai une analyse détaillée des impacts et mesures d'atténuation.")
            
            for msg in historique:
                timestamp_str = msg['timestamp'].strftime("%H:%M:%S")
                
                if msg['type'] == 'user':
                    with st.chat_message("user"):
                        st.write(f"**{timestamp_str}** - {msg['contenu']}")
                else:
                    with st.chat_message("assistant"):
                        st.write(f"**{timestamp_str}**")
                        st.markdown(msg['contenu'])
        
        # Zone de saisie
        st.markdown("### ✍️ Votre question")
        
        with st.form(key="message_form", clear_on_submit=True):
            user_input = st.text_area(
                "Décrivez votre projet autoroutier :",
                height=120,
                placeholder="Exemple : Nous planifions la construction d'une nouvelle section autoroutière avec terrassement important, traversée de cours d'eau et circulation intense d'engins. Quels sont les principaux impacts sur l'eau et l'air ?",
                key="user_input"
            )
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                submitted = st.form_submit_button(
                    "🚀 Analyser", 
                    use_container_width=True,
                    type="primary"
                )
        
        # Traitement du message
        if submitted and user_input.strip():
            with st.spinner("🔍 Analyse environnementale en cours..."):
                chatbot.traiter_conversation(user_input.strip())
            st.rerun()
        elif submitted and not user_input.strip():
            st.warning("⚠️ Veuillez décrire votre projet avant de lancer l'analyse.")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "*Assistant IA basé sur les meilleures pratiques d'évaluation environnementale autoroutière*",
            help="Cet outil utilise une base de connaissances spécialisée pour fournir des analyses personnalisées selon votre projet."
        )

    main()
if __name__ == "__main__":
>>>>>>> 9ba0955f04e86c2f7e986ab511406cd53ae3e8d1
    run()