# Criar uma cópia do DataFrame filtrado para edição
df_doadores_modificado = df_doadores.copy()

# Substituir cada PDSID pelo outro Inventory BID vinculado no DataFrame original
for col in df_doadores_modificado.columns:
    if "PDSID" in col:
        df_doadores_modificado[col] = df_doadores_modificado[col].apply(
            lambda pdsid: ', '.join([bid for bid in pdsid_to_bid.get(pdsid, []) 
                                     if bid not in df_doadores_modificado["Inventory BID"].values])
            if pdsid in pdsid_to_bid else pdsid
        )

# Exibir o DataFrame atualizado
tools.display_dataframe_to_user(name="Plantas Doadoras Atualizadas", dataframe=df_doadores_modificado)
