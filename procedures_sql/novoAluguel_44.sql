CREATE PROCEDURE novoAluguel_44(
    vClienteNome VARCHAR(150),
    vHospedagem VARCHAR(10),
    vDataInicio DATE,
    vDias INTEGER,
    vPrecoUnitario DECIMAL(10,2)
)
BEGIN
    -- Validação do cliente
    SET vNumCliente = (SELECT COUNT(*) FROM clientes WHERE nome = vClienteNome);

    CASE
        WHEN vNumCliente = 0 THEN
            SELECT 'Cliente não existe';
        WHEN vNumCliente = 1 THEN
            -- Geração de novo ID
            SELECT CAST(MAX(CAST(aluguel_id AS UNSIGNED))+1 AS CHAR) INTO vAluguel FROM alugueis;

            -- Cálculo da data final
            CALL calculaDataFinal_43(vDias, vDataInicio, vDataFinal);

            -- Cálculo do valor total
            SET vPrecoTotal = vDias * vPrecoUnitario;

            -- Inserção do aluguel
            SELECT cliente_id INTO vCliente FROM clientes WHERE nome = vClienteNome;
            INSERT INTO alugueis VALUES (
                vAluguel, vCliente, vHospedagem, vDataInicio, vDataFinal, vPrecoTotal
            );

            SELECT CONCAT('Aluguel incluído com sucesso. ID: ', vAluguel);
        ELSE
            SELECT 'Cliente duplicado. Nome não pode ser usado.';
    END CASE;
END;
