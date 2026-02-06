from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Spesa, Categoria


@api_view(['POST'])
def crea_spesa(request):
    descrizione = request.data.get('descrizione')
    importo = request.data.get('importo')
    data_str = request.data.get('data')
    categoria_id = request.data.get('categoria_id')
    note = request.data.get('note', '')

    # Validazioni
    if not descrizione or importo is None or not data_str or not categoria_id:
        return Response({"errore": "Campi obbligatori mancanti"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"errore": "Formato data errato, usare YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        categoria = Categoria.objects.get(pk=categoria_id)
    except Categoria.DoesNotExist:
        return Response({"errore": "Categoria non trovata"}, status=status.HTTP_404_NOT_FOUND)

    spesa = Spesa.objects.create(
        descrizione=descrizione,
        importo=importo,
        data=data,
        categoria=categoria,
        note=note
    )

    return Response({
        "id": str(spesa.id),
        "descrizione": spesa.descrizione,
        "importo": float(spesa.importo),
        "data": spesa.data.isoformat(),
        "categoria": spesa.categoria.nome,
        "note": spesa.note
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def spese_per_categorie(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response({"errore": "Categoria non trovata"}, status=status.HTTP_404_NOT_FOUND)

    spese = categoria.spese.all()
    lista = [{
        "id": str(s.id),
        "descrizione": s.descrizione,
        "importo": float(s.importo),
        "data": s.data.isoformat(),
        "note": s.note
    } for s in spese]

    return Response(lista, status=status.HTTP_200_OK)


@api_view(['GET'])
def spese_mese(request):
    mese = request.query_params.get('mese')  # formato YYYY-MM
    if not mese:
        return Response({"errore": "Parametro 'mese' obbligatorio"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        anno, mese_int = map(int, mese.split('-'))
    except:
        return Response({"errore": "Formato mese errato, usare YYYY-MM"}, status=status.HTTP_400_BAD_REQUEST)

    spese = Spesa.objects.filter(data__year=anno, data__month=mese_int)
    lista = [{
        "id": str(s.id),
        "descrizione": s.descrizione,
        "importo": float(s.importo),
        "data": s.data.isoformat(),
        "categoria": s.categoria.nome,
        "note": s.note
    } for s in spese]

    return Response(lista, status=status.HTTP_200_OK)


@api_view(['GET'])
def budget_residuo_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response({"errore": "Categoria non trovata"}, status=status.HTTP_404_NOT_FOUND)

    totale_spese = sum(s.importo for s in categoria.spese.all())
    residuo = float(categoria.budget_mensile) - float(totale_spese)

    return Response({
        "categoria": categoria.nome,
        "budget_mensile": float(categoria.budget_mensile),
        "totale_spese": float(totale_spese),
        "budget_residuo": residuo
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def totale_spese_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return Response({"errore": "Categoria non trovata"}, status=status.HTTP_404_NOT_FOUND)

    totale = sum(s.importo for s in categoria.spese.all())
    return Response({
        "categoria": categoria.nome,
        "totale_spese": float(totale)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def dettagli_spesa(request, id):
    try:
        spesa = Spesa.objects.get(id=id)
    except Spesa.DoesNotExist:
        return Response({"errore": "Spesa non trovata"}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "id": str(spesa.id),
        "descrizione": spesa.descrizione,
        "importo": float(spesa.importo),
        "data": spesa.data.isoformat(),
        "categoria": spesa.categoria.nome,
        "note": spesa.note
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def modifica_spesa(request, id):
    try:
        spesa = Spesa.objects.get(id=id)
    except Spesa.DoesNotExist:
        return Response({"errore": "Spesa non trovata"}, status=status.HTTP_404_NOT_FOUND)

    spesa.descrizione = request.data.get('descrizione', spesa.descrizione)
    spesa.importo = request.data.get('importo', spesa.importo)
    data_str = request.data.get('data')
    if data_str:
        try:
            spesa.data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"errore": "Formato data errato, usare YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    categoria_id = request.data.get('categoria_id')
    if categoria_id:
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            spesa.categoria = categoria
        except Categoria.DoesNotExist:
            return Response({"errore": "Categoria non trovata"}, status=status.HTTP_404_NOT_FOUND)

    spesa.note = request.data.get('note', spesa.note)
    spesa.save()

    return Response({
        "id": str(spesa.id),
        "descrizione": spesa.descrizione,
        "importo": float(spesa.importo),
        "data": spesa.data.isoformat(),
        "categoria": spesa.categoria.nome,
        "note": spesa.note
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def elimina_spesa(request, id):
    try:
        spesa = Spesa.objects.get(id=id)
    except Spesa.DoesNotExist:
        return Response({"errore": "Spesa non trovata"}, status=status.HTTP_404_NOT_FOUND)

    spesa.delete()
    return Response({"successo": f"Spesa '{spesa.descrizione}' eliminata"}, status=status.HTTP_200_OK)
