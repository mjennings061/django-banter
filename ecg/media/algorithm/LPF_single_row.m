function LPF_single_row(filePath)
    dataIn = csvread(filePath);
    dataOut = dataIn + 0.5;
    csvwrite('LPF_single_row_result.csv',dataOut)
end