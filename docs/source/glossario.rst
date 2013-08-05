
Glossário
=========

.. glossary::

    Cupom fiscal

        Documento emitido por um ECF, para o fisco, que representa uma venda realizada.

        Exemplo de cupom::

                        NOME DA EMPRESA LTDA
              ENDERECO DO CLIENTE, BAIRRO , Nº 001
                    ALGUM BAIRRO - SAO PAULO - SP

            CNPJ:50.600.206/0001-70
            IE:100.800.956.213
            ------------------------------------------------
            01/03/2013 00:02:03   CCF:110639      COO:116503
                  CUPOM FISCAL
            ITEM CÓDIGO DESCRIÇÃO QTD.UN.VL UNIT( R$) ST VL ITEM( R$)
            ------------------------------------------------
            001 273 FRANGO GREL COMPLETO 1UN I1                62,00G
            002 99 CHOP GUINNESS 400ML 2DOx19,00 F1            38,00G
            003 155 SUCOS DIVERSOS 1UN I1                       5,90G
            004 266 FAROFA 1UN T08,40%                          8,00G
                                          ------------------
            TOTAL  R$                                113,90
            VISA CREDITO                              62,64
            VISA ELECTRON                             62,64
            SOMA                                     125,28
            TROCO  R$                                 11,38
            MD5-2af2b86eb6cbe9b8084c169d0ddda184
            Mesa : 075 Sequencia : 167
                          1987 / 2012
                          " 25 ANOS "
                     NAO ACEITAMOS CHEQUES
            ---------Colibri Food - Versao 6.80.8.35
            ------------------------------------------------
            BEMATECH MP-2100 TH FI ECF-IF
            VERSÃO:01.01.01 ECF:003 LJ:0001
            QQQQQQQQWRWQYRRQWQ 01/03/2013 00:02:06
            FAB:BE000000000000000001                     BR


    Redução Z

        Documento emitido por um ECF, para o fisco, que representa o resumo das vendas realizadas
        em uma jornada de trabalho.

        Exemplo de Redução Z::

                        NOME DA EMPRESA LTDA
              ENDERECO DO CLIENTE, BAIRRO , Nº 001
                    ALGUM BAIRRO - SAO PAULO - SP

            CNPJ:50.600.206/0001-70
            IE:100.800.956.213
            ------------------------------------------------
            01/03/2013 08:45:25                   COO:116506
                   REDUÇÃO Z
            MOVIMENTO DO DIA: 28/02/2013
                               CONTADORES
            Geral de Operação Não-Fiscal:             003855
            Contador de Reinício de Operação:            002
            Contador de Reduções Z:                     1246
            Contador de Cupom Fiscal:                 110641
            Contador de Fita-Detalhe:                 000000
            Comprovante de Crédito ou Débito:           0000
            Geral de Relatório Gerencial:             000673
            Geral Oper. Não-Fiscal Canc.:               0000
            Cupom Fiscal Cancelado:                     0000
                             TOTALIZADORES
            TOTALIZADOR GERAL:                 13.105.507,00
            VENDA BRUTA DIÁRIA:                    10.036,70
            CANCELAMENTO ICMS:                          0,00
            DESCONTO ICMS:                              0,00
            Total de ISSQN:                             0,00
            CANCELAMENTO ISSQN:                         0,00
            DESCONTO ISSQN:                             0,00
                                          ------------------
            VENDA LÍQUIDA:                         10.036,70
            ACRÉSCIMO ICMS:                             0,00
            ACRÉSCIMO ISSQN:                            0,00
                                  ICMS
            Totalizador Base Cálculo( R$)       Imposto( R$)
            T08,40%              1.765,50             148,30
            T12,00%                  0,00               0,00
            T18,00%                  0,00               0,00
            T25,00%                  0,00               0,00
                                          ------------------
            Total ICMS:          1.765,50             148,30
            Não Tributados             Valor Acumulado( R$)
            F1 =                                    4.904,60
            I1 =                                    3.366,60
            N1 =                                        0,00
                                 ISSQN
            Totalizador Base Cálculo( R$)       Imposto( R$)
                                          ------------------
            Total ISSQN:             0,00               0,00
            Não Tributados             Valor Acumulado( R$)
            FS1 =                                       0,00
            IS1 =                                       0,00
            NS1 =                                       0,00
                       TOTALIZADORES NÃO FISCAIS
            Nº Operação             CON Valor Acumulado( R$)
            01 Assinada           : 0000                0,00
            02 Contra-vale        : 0000                0,00
            03 Repique            : 0000                0,00
            29 Sangria            : 0002            5.928,31
            30 Suprimento         : 0002              117,51
                                          ------------------
            Total Oper Não-Fiscais                  6.045,82
            ACRE NÃO-FISC                               0,00
            DESC NÃO-FISC                               0,00
            CANC NÃO-FISC                               0,00
                          RELATÓRIO GERENCIAL
            Nº Relatório                                CER
            01 Relatório Geral                          0000
            02 Conf. de mesa                            0000
            03 Conf. de ficha                           0000
            04 Mesas em aberto                          0000
            05 Fichas abertas                           0000
            06 Transf. mesas                            0000
            07 Reg. venda/canc                          0000
            08 Fech. operador                           0000
            09 Fech. periodo                            0000
            10 Recibo pgto.                             0000
            11 TEF                                      0000
            12 Ident. PAF-ECF                           0000
                           MEIOS DE PAGAMENTO
            Nº   Meio Pagamento        Valor Acumulado ( R$)
            01    Dinheiro                          6.570,21
            02    CHEQUE           (V)                  0,00
            03    CONTRA-VALE      (V)                  0,00
            04    REDESHOP         (V)                  0,00
            05    VISA CREDITO     (V)              1.251,14
            06    AMEX             (V)                666,38
            07    VISA ELECTRON    (V)                912,38
            08    MASTERCARD       (V)              1.194,08
            09    Conta Assinada   (V)                 21,00
            10    PAGAMENTO A MEN  (V)                  0,00
            11    TICKET PAPEL     (V)                  0,00
            12    CONTRA VALE      (V)                  0,00
            13    TR ELETRONICO    (V)                  0,00
            14    DINNERS          (V)                  0,00
            15    SINAL            (V)                  0,00
            TROCO                                     460,98
            Comprovante Não Emitido:                    0035
            Tempo Emitindo Doc. Fiscal:             00:01:36
            Tempo Operacional:                      08:31:22
            Qtd. Reduções Restantes:                    0798
            Número série MFD:67600804100923
            ------------------------------------------------
            BEMATECH MP-2100 TH FI ECF-IF
            VERSÃO:01.01.01 ECF:003 LJ:0001
            QQQQQQQQWRWQYYQIQQ 01/03/2013 08:45:46
            FAB:BE000000000000000001                     BR


    Espelho MFD

        Arquivo que contém os dados de todos os documentos emitidos por um ECF dentro
        do período especificado na geração do arquivo. O arquivo tem este nome pois
        segue o mesmo formato dos dados que foram impressos no equipamento.