function y = LPF_single_row(filePath)
    dataIn = csvread(filePath); % read from a CSV file
    dataOut = dataIn + 0.5; % add 0.5 to each data point
    csvwrite(['C:\Users\MJ\OneDrive - Ulster University\' ...
        'Documents\PhD\Django\django-banter\ecg\media\results\' ...
        'LPF_single_row_result.csv'],dataOut);  % save to CSV file
    y = 1;  % return function was successful
end
