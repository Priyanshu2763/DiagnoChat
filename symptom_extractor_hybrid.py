import re
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from rapidfuzz import process
# import joblib

# Load small spaCy model (for stopwords)
nlp = spacy.load("en_core_web_sm")

def preprocess(user_input: str) -> str:
    """
    Preprocess user input:
    - Lowercase
    - Remove punctuation
    - Remove stopwords
    - Remove extra spaces
    - Return clean sentence
    """
    # Lowercase
    text = user_input.lower().strip()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Tokenize with spaCy
    doc = nlp(text)

    # Remove stopwords and normalize spacing
    tokens = [token.text for token in doc if not token.is_stop]

    # Join back into string
    clean_text = " ".join(tokens)

    # Remove multiple spaces (if any)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return clean_text


def synonym_match(text: str) -> str:
    """
    Replace known multi-word and single-word synonyms in the input text.
    Args:
        text (str): preprocessed user input
    Returns:
        str: text with synonyms replaced
    """
    synonym_dict = {
        # Fever family
        "feverish": "fever",
        "high temperature": "fever",
        "temperature": "fever",

        # Headache family
        "head pain": "headache",
        "migraine": "headache",
        "head is hurting": "headache",

        # Fatigue family
        "tired": "fatigue",
        "exhausted": "fatigue",
        "weakness": "fatigue",
        "lathargic": "fatigue",
        "lack of energy": "fatigue",
         "high temperature": "fever",
    "temperature": "fever",
    "raised temperature": "fever",
    "tiredness": "fatigue",
    "feeling tired": "fatigue",
    "weakness": "fatigue",
    "runny nose": "rhinorrhea",
    "stuffy nose": "nasal congestion",
    "blocked nose": "nasal congestion",
    "difficulty breathing": "shortness of breath",
    "trouble breathing": "shortness of breath",
    "short of breath": "shortness of breath",
    "no sense of smell": "anosmia",
    "lost sense of smell": "anosmia",
    "lost sense of taste": "ageusia",
    "sore throat": "sore throat",
    "painful swallowing": "sore throat",
    "nauseous": "nausea",
    "throwing up": "vomiting",
    "vomit": "vomiting",
    "head ache": "headache",
    "head-ache": "headache",
    "backache": "back pain",
    "stomach ache": "abdominal pain",
    "stomachache": "abdominal pain",
    "belly pain": "abdominal pain",
    "blood in urine": "hematuria",
    "blood in stool": "hematochezia",
    "skin rash": "rash",
    "itching": "itching",
    "itchy": "itching",
    "chest pain": "chest pain",
    "palpitations": "palpitation",
    "fast heart rate": "tachycardia",
    "frequent urination": "urinary_frequency",
    "painful urination": "dysuria",
    "pain when urinating": "dysuria",
    "sudden weight loss": "weight loss",
    "weight loss unexplained": "weight loss",
    "swollen glands": "lymphadenopathy",
    "swollen lymph nodes": "lymphadenopathy",
    "bleeding after sex": "postcoital_bleeding",
    "bleeding between periods": "intermenstrual_bleeding",
    "period pain": "dysmenorrhea",
    "period cramps": "dysmenorrhea",
    "feverish": "fever",
    }

    # Replace phrases (longer phrases first)
    for phrase in sorted(synonym_dict.keys(), key=lambda x: -len(x)):
        if phrase in text:
            text = text.replace(phrase, synonym_dict[phrase])

    return text


lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to WordNet POS for better lemmatization"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_symptoms(symptom_list):
    """
    Lemmatize each symptom in the list.
    Example: ['sneezed', 'coughing', 'headaches'] -> ['sneeze', 'cough', 'headache']
    """
    lemmatized = []
    for s in symptom_list:
        words = s.split()  # in case of multi-word symptom
        lemma_words = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in words]
        lemmatized.append(" ".join(lemma_words))
    return lemmatized


def fuzzy_match(symptom_list, valid_symptoms, threshold=80):
    """
    Fuzzy match user symptoms to known dataset symptoms.
    
    Args:
        symptom_list (list): user input symptoms (preprocessed/lemmatized)
        valid_symptoms (list): list of valid symptoms from dataset (symptom_columns.pkl)
        threshold (int): minimum match score (0-100)
    
    Returns:
        matched (list): list of matched symptoms from dataset
        unmatched (list): symptoms that could not be matched
    """
    matched = []
    unmatched = []

    for s in symptom_list:
        # Find best match
        best_match, score, _ = process.extractOne(s, valid_symptoms)
        if score >= threshold:
            matched.append(best_match)
        else:
            unmatched.append(s)

    return matched, unmatched
ambiguity_dict = {
    "cough": ["dry cough", "wet cough", "cough", "persistent cough"],
    "pain": ["headache", "chest pain", "abdominal pain", "back pain", "joint pain", "throat pain"],
    "ache": ["headache", "stomach ache", "toothache", "earache", "body ache"],
    "rash": ["skin rash", "facial rash", "red rash", "itchy rash", "blistering rash"],
    "nose": ["runny nose", "blocked nose", "bleeding nose"]
}
def resolve_ambiguity(symptoms, valid_symptoms):
    resolved = []
    for s in symptoms:
        if s in ambiguity_dict:
            options = [opt for opt in ambiguity_dict[s] if opt in valid_symptoms]
            if options:
                print(f"⚠️ Ambiguity detected for '{s}'. Please choose one:")
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")
                choice = input("Enter the number of the correct option: ")
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(options):
                        resolved.append(options[choice_idx])
                    else:
                        resolved.append(s)  # fallback
                except ValueError:
                    resolved.append(s)  # fallback
            else:
                resolved.append(s)
        else:
            resolved.append(s)
    return resolved


def extract_symptoms(user_input, valid_symptoms):
    # Preprocess
    clean_text = preprocess(user_input)
    
    # Step 1b: Correct typos
    # clean_text = correct_typos(clean_text)
    clean_text = synonym_match(clean_text)

    matched = []

    # Step 2: Exact match multi-word symptoms first
    temp_text = clean_text
    for symptom in sorted(valid_symptoms, key=lambda x: -len(x)):  # longer first
        if symptom in temp_text:
            matched.append(symptom)
            temp_text = temp_text.replace(symptom, "")  # remove to avoid duplicates

    # Step 3: Split remaining text into tokens
    remaining_tokens = [t for t in temp_text.split() if t]

    # Step 4: Synonym matching on remaining tokens
    normalized = synonym_match(remaining_tokens)

    # Step 5: Lemmatize
    lemmatized_tokens = lemmatize_symptoms(normalized)

    # Step 6: Fuzzy matching only if few matched symptoms
    fuzzy_matched = []
    if len(matched) < 2 and lemmatized_tokens:
        fuzzy_matched, _ = fuzzy_match(lemmatized_tokens, valid_symptoms)
    
    matched += fuzzy_matched
    unmatched = [t for t in lemmatized_tokens if t not in fuzzy_matched]

    # return matched, unmatched
    matched = resolve_ambiguity(matched, valid_symptoms)
    return matched



# if __name__ == "__main__":
    # user_sentence = "I have runny nose, sore throat and head pain and i am feeling feverish"
    
    # matched, unmatched = extract_symptoms(user_sentence, valid_symptoms)

    # print("✅ Extracted Symptoms:", matched)
    # print("❌ Could Not Match:", unmatched)