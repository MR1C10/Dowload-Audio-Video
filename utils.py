def limpar_nome(nome):
    return "".join(c for c in nome if c.isalnum() or c in " ._-").rstrip()
