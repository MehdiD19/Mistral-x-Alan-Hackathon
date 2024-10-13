ef generate_few_shot_examples() -> str:
    # These would ideally be actual examples from your dataset
    return """
Example 1:
Q : Quelle est la cause la plus fréquente de pneumonie acquise en communauté chez les adultes ?
A. Streptococcus pneumoniae
B. Haemophilus influenzae
C. Mycoplasma pneumoniae
D. Legionella pneumophila
E. Staphylococcus aureus
Réponse correcte : A

"Q : Concernant l'intoxication aiguë par l'amitriptyline, quelle(s) est (sont) la (les) proposition(s) exacte(s) ?
A. Un syndrome sérotoninergique est observé
B. Un syndrome anticholinergique est observé
C. Des convulsions peuvent être observées
D. Le pronostic dépend des troubles cardiovasculaires
E. La dose toxique est supérieure à 5 grammes chez l'adulte
Réponse correcte : A, B, C, D
"""

def generate_answer(question: str, options , examples: str) -> str:
    prompt = f"""Vous êtes un professeur expert en médecine chargé de répondre aux questions des examens de médecine. Regardez les examples suivants pour vous aider à répondre à la question ci-dessous et :

{examples}

Maintenant, répondez aux questions suivantes :

Question: {question}

Options:
A. {options['A']}
B. {options['B']}
C. {options['C']}
D. {options['D']}
E. {options['E']}


Fournissez votre réponse dans le format suivant :

1.Indiquez les bonnes/ la bonne réponses puisque c'est un QCM à choix multiples (A, B, C, D ou E). Donner que les lettres correpondants aux bonnes réponses, seulement les lettres, pas d'explication ni rien d'autre.
2.Fournissez une brève explication de pourquoi c'est la bonne réponse.
3.Expliquez pourquoi les autres options sont incorrectes.
4.Indiquez votre niveau de confiance dans votre réponse (0-100%).
5.Pourquoi avez-vous choisi ce niveau de confiance ?
5.Réfléchissez étape par étape avant de fournir votre réponse final  """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    
    data = {
        "model": "mistral-large-2407",  # Using a more capable model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3  # Lower temperature for more focused answers
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    csv_file_path = "questions.csv"
    questions = read_csv(csv_file_path)
    few_shot_examples = generate_few_shot_examples()
    
    results = []
    for i, q in enumerate(questions, 1):
        print(f"\nProcessing question {i}...")
        answer = generate_answer(q['question'], {
            'A': q['answer_A'], 'B': q['answer_B'], 'C': q['answer_C'], 'D': q['answer_D'], 'E': q['answer_E']
        }, few_shot_examples)
        results.append({
            'question': q['question'],
            'answer': answer
        })
        time.sleep(2)
        print(f"Question: {q['question']}")
        print(f"Generated Answer: {answer}")
    
    df = pd.DataFrame(results)
    df.to_csv('answers.csv', index=False)
    print("Answers saved to answers.csv")

if __name__ == "__main__":
    main()

