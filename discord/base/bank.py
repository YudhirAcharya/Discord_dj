from transformers import pipeline
import re

# Define the calculations
def calculate_emi(P: float, r: float, n: int) -> float:
    """Calculate Equated Monthly Installment (EMI)."""
    r = r / 12 / 100  # Convert annual interest rate to monthly and to decimal
    emi = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return emi

def calculate_simple_interest(P: float, r: float, t: float) -> float:
    """Calculate Simple Interest."""
    si = P * r * t
    return si

def calculate_compound_interest(P: float, r: float, n: int, t: float) -> float:
    """Calculate Compound Interest."""
    ci = P * (1 + r / n) ** (n * t) - P
    return ci

# Function to parse input and identify parameters
def extract_parameters(text: str):
    params = {}
    patterns = {
        'P': r'(\d+(\.\d+)?)\s*(principal|amount|loan)',
        'r': r'(\d+(\.\d+)?)\s*%',
        'n': r'(\d+(\.\d+)?)\s*(years?|months?|annually|compounded)',
        't': r'(\d+(\.\d+)?)\s*(years?|months?|annually|compounded)',
    }
    
    # Mapping for synonyms and abbreviations
    synonyms = {
        'principal': 'P',
        'amount': 'P',
        'loan': 'P',
        'rate': 'r',
        'interest': 'r',
        'time': 't',
        'years': 't',
        'months': 't',
        'annual': 'n',
        'compounded': 'n',
        'compounding': 'n',
        'compounds': 'n',
        'installments': 'n',
    }
    
    # Combine main patterns and synonyms for a comprehensive search
    combined_patterns = {**patterns, **{synonym: patterns[param] for synonym, param in synonyms.items()}}
    
    # Additional context-aware patterns
    for param, pattern in combined_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            params[param] = float(match.group(1))
    
    # Fallback to param=value format
    for param in ['P', 'r', 'n', 't']:
        if param not in params:
            match = re.search(rf'{param}\s*=\s*(\d+(\.\d+)?)', text, re.IGNORECASE)
            if match:
                params[param] = float(match.group(1))
    
    return params

# Function to determine the type of calculation
def determine_calculation(text: str):
    if "emi" in text.lower():
        return "emi"
    elif "simple interest" in text.lower():
        return "simple_interest"
    elif "compound interest" in text.lower():
        return "compound_interest"
    else:
        return None

def main():
    nlp = pipeline("text-classification")

    while True:
        text = input("Enter your query (or 'exit' to quit): ")
        if text.lower() == 'exit':
            break

        calculation_type = determine_calculation(text)
        params = extract_parameters(text)

        if calculation_type == "emi":
            if 'P' in params and 'r' in params and 'n' in params:
                result = calculate_emi(params['P'], params['r'], int(params['n']))
                print(f"EMI: {result:.2f}")
            else:
                print("Insufficient parameters for EMI calculation.")

        elif calculation_type == "simple_interest":
            if 'P' in params and 'r' in params and 't' in params:
                result = calculate_simple_interest(params['P'], params['r'], params['t'])
                print(f"Simple Interest: {result:.2f}")
            else:
                print("Insufficient parameters for Simple Interest calculation.")

        elif calculation_type == "compound_interest":
            if 'P' in params and 'r' in params and 'n' in params and 't' in params:
                result = calculate_compound_interest(params['P'], params['r'], int(params['n']), params['t'])
                print(f"Compound Interest: {result:.2f}")
            else:
                print("Insufficient parameters for Compound Interest calculation.")

        else:
            print("Unknown calculation type.")

if __name__ == "__main__":
    main()
