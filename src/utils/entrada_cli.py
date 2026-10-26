def converter_peso(texto):
    """Converte um peso digitado com ponto ou vírgula decimal."""
    try:
        return float(texto.strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError(
            "Digite um peso numérico, por exemplo 5 ou 2,5."
        ) from None