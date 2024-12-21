import matplotlib.pyplot as plt
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sympy import sympify, lambdify, Symbol
import os
import uuid
import re  # Import regular expressions module

def index(request):
    context = {"image": 0,"polynomial":""}
    
    if request.method == 'POST':
        # Récupérer le polynôme envoyé depuis le frontend
        polynomial = request.POST.get('fonction')
        print(polynomial)
        if not polynomial:
             return render(request, 'index.html', context)
        context["polynomial"]=polynomial
        # Convert the polynomial to lowercase
        polynomial = polynomial.lower()
        

        # Preprocess the polynomial to add explicit multiplication
        polynomial = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', polynomial)
        print(f"Processed polynomial: {polynomial}")
        
        try:
            # Utiliser SymPy pour analyser le polynôme de manière sécurisée
            x = Symbol('x')  # Variable symbolique
            expr = sympify(polynomial)  # Convertir la chaîne en expression mathématique
            func = lambdify(x, expr, 'numpy')  # Transformer l'expression en une fonction Python/Numpy

            # Calculer les valeurs pour le tracé
            x_vals = np.linspace(-10, 10, 500)  # Points sur l'axe x
            y_vals = func(x_vals)  # Calcul des valeurs y correspondantes

            # Créer le graphique
            plt.figure()
            plt.plot(x_vals, y_vals, label=f'y = {expr}')
            plt.title('Graphique du Polynôme')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.legend()
            plt.grid(True)

            # Générer un nom unique pour le fichier image
            filename = f"polynomial_{uuid.uuid4().hex}.png"
            filepath = os.path.join('media', filename)

            # Sauvegarder l'image dans le dossier 'media'
            plt.savefig(filepath)
            plt.close()
            context["image"] = filepath  # Update context with the image path
            
            # Retourner le chemin de l'image pour affichage
            return render(request, 'index.html', context)

        except Exception as e:
            # Gestion des erreurs (par exemple, polynôme invalide)
            print(e)
            return JsonResponse({'error': f"Erreur : {str(e)}"})

    # Si ce n'est pas une requête POST, rendre la page avec le formulaire
    return render(request, 'index.html')
