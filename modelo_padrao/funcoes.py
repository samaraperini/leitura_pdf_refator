import os
import re
import expressao_regular
import pdf
import constantes

def ler_arquivos(nome_arquivo):
    for arquivos in nome_arquivo:
        caminho_arquivo = os.path.join(constantes.PASTA_INPUT, arquivos)
        texto_pdf = pdf.obter_texto_arquivo_pdf(caminho_arquivo)
        valor = expressao_regular.encontrar_combinacao_grupo(constantes.VALOR_CAUSA,texto_pdf)
        valor = re.sub(r"\s+", "", valor)
        valor = valor.split(':')
        constantes.valor_causa.append((valor [-1]).replace('R$',''))
        parte_credora = expressao_regular.encontrar_combinacao_grupo(constantes.PARTE_CREDORA,texto_pdf)
        parte_credora = parte_credora.replace('\n','').split(':')
        constantes.credor.append(parte_credora [-1])
        documento_credor = expressao_regular.encontrar_combinacao_grupo(constantes.DOCUMENTO_CREDOR ,texto_pdf)
        documento_credor = re.sub(r"\s+", "", documento_credor)
        documento_credor = documento_credor.split(':')
        constantes.documento.append(documento_credor[-1])
        advogado = expressao_regular.encontrar_combinacao_grupo(constantes.ADVOGADO,texto_pdf)
        advogado = advogado.replace('\n','').split(':')
        constantes.adv.append(advogado[-1])
        documento_adv = expressao_regular.encontrar_combinacao_grupo(constantes.DOCUMENTO_ADV ,texto_pdf)
        documento_adv = re.sub(r"\s+", "", documento_adv)
        documento_adv = documento_adv.split(':')
        constantes.doc_adv.append(documento_adv[-1])
        oab = expressao_regular.encontrar_combinacao_grupo(constantes.OAB,texto_pdf)
        oab = re.sub(r"\s+", "", oab)
        oab = oab.split(':')
        constantes.adv_oab.append(oab [-1])
        natureza = expressao_regular.encontrar_todas_combinacoes(constantes.NATUREZA, texto_pdf)
        if natureza is not None:
            constantes.natureza_do_precatorio.append('ALIMENTAR')
        else:
            constantes.natureza_do_precatorio.append('COMUM')
        vl_principal = expressao_regular.encontrar_combinacao_grupo(constantes.VL_PRINCIPAL,texto_pdf)
        vl_principal = re.sub(r"\s+", "", vl_principal).replace('Juros:','')
        vl_principal = vl_principal.split(':')
        if len(vl_principal) == 2:    
            constantes.valor_principal.append((vl_principal[1]).replace('R$',''))
        else:
            constantes.valor_principal.append('0,00')
        vl_juros = expressao_regular.encontrar_combinacao_grupo(constantes.VL_JUROS,texto_pdf)
        vl_juros = re.sub(r"\s+", "", vl_juros).replace('Índices/taxaSelic:','')
        vl_juros = vl_juros.split(':')
        if len(vl_juros) == 2:
            if (vl_juros[1]) == 'R$':
                constantes.valor_juros.append('0,00')
            else: constantes.valor_juros.append((vl_juros[1]).replace('R$',''))
        else: constantes.valor_juros.append('0,00')
        try:
            data_bs = expressao_regular.encontrar_combinacao_grupo(constantes.DATA_BASE,texto_pdf)
            data_bs = data_bs.split(':')  
            constantes.data_base.append((data_bs[1]).replace('\n ','').replace('.','/'))
        except:
            constantes.data_base.append('01/01/1900')
        totall = expressao_regular.encontrar_combinacao_grupo(constantes.TOTAL, texto_pdf)
        totall = totall.replace('DADOS COMPLEMENTARES','')
        totall = totall.split('\n')
        constantes.total.append(totall[2])
        honorario_adv = expressao_regular.encontrar_combinacao_grupo(constantes.HONORARIO, texto_pdf)
        honorario_adv = honorario_adv.replace('Total da Requisição','')
        honorario_adv = honorario_adv.split('\n')
        constantes.honorario.append(honorario_adv[3])
        constantes.porcentagem_honorario.append(honorario_adv[4])
        constantes.valor_honorario.append(honorario_adv[5])
        print(arquivos, 'tratado!')
    resultado = {'Data base': constantes.data_base,'Valor da causa': constantes.valor_causa, 'Valor Principal': constantes.valor_principal, 'Valor Juros': constantes.valor_juros, 'Valor Total' : constantes.total,'Beneficiário': constantes.credor, 'Documento': constantes.documento, 'Natureza' : constantes.natureza_do_precatorio, 'Advogado': constantes.adv, 'Adv Documento': constantes.doc_adv, 'OAB': constantes.adv_oab, 'Honorário': constantes.honorario, '% Honorário': constantes.porcentagem_honorario, 'Valor Honorário': constantes.valor_honorario}
    return resultado
        
