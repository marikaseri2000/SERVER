from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria

@api_view(['POST'])
def crea_categoria(request):
    """
    Crea una nuova categoria con nome e budget mensile opzionale.
    """
    nome = request.data.get('nome')
    budget = request.data.get('budget_mensile', 0.00)  # opzionale, default 0.00

    # Controllo obbligatorietà nome
    if not nome:
        return Response(
            {"errore": "Il campo 'nome' è obbligatorio"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Evita duplicati
    if Categoria.objects.filter(nome=nome).exists():
        return Response(
            {"errore": "Categoria già esistente"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Creazione categoria
    try:
        categoria = Categoria.objects.create(
            nome=nome,
            budget_mensile=budget
        )
    except Exception as e:
        return Response(
            {"errore": f"Errore durante la creazione: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Risposta con dati creati
    return Response(
        {
            "id": categoria.id,
            "nome": categoria.nome,
            "budget_mensile": float(categoria.budget_mensile)
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def lista_categorie(request):
    """Restituisce tutte le categorie con ID, nome e budget mensile."""
    categorie = Categoria.objects.all()

    # Creiamo una lista di dizionari
    lista = [
        {
            "id": c.id,
            "nome": c.nome,
            "budget_mensile": float(c.budget_mensile)
        }
        for c in categorie
    ]

    return Response(lista, status=status.HTTP_200_OK)


@api_view(['GET'])
def dettagli_categoria(request, id):
    """
    Restituisce i dettagli di una categoria dato l'ID.
    """
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response(
            {"errore": "Categoria non trovata"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "id": categoria.id,
            "nome": categoria.nome,
            "budget_mensile": float(categoria.budget_mensile)
        },
        status=status.HTTP_200_OK
    )

@api_view(['PATCH'])
def modifica_categoria(request, id):
    """
    Aggiorna nome o budget_mensile di una categoria esistente.
    Modifica parziale dei campi.
    """
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response(
            {"errore": "Categoria non trovata"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Legge i valori dal body, se presenti
    nome = request.data.get('nome', categoria.nome)
    budget = request.data.get('budget_mensile', categoria.budget_mensile)

    # Controlla duplicati solo se il nome cambia
    if nome != categoria.nome and Categoria.objects.filter(nome=nome).exists():
        return Response(
            {"errore": "Nome già esistente"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Aggiorna e salva
    categoria.nome = nome
    categoria.budget_mensile = budget
    categoria.save()

    return Response(
        {
            "id": categoria.id,
            "nome": categoria.nome,
            "budget_mensile": float(categoria.budget_mensile)
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def elimina_categoria(request, id):
    """Elimina una categoria dal database."""
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response(
            {"errore": "Categoria non trovata"},
            status=status.HTTP_404_NOT_FOUND
        )

    categoria.delete()

    return Response(
        {"successo": f"Categoria '{categoria.nome}' eliminata"},
        status=status.HTTP_200_OK
    )

