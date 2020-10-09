function y = take_half(filePath)
    fclose('all');
    %% function operations
    dataIn = csvread(filePath); % read from a CSV file
    dataOut = dataIn - 0.5; % add 0.5 to each data point
    
    %% Django-specific operations
    rng('shuffle');     % to help prevent the same 'random number'
    id = randi(2^32);   % generate a random number as the file ID
    path_dir = ['C:/Users/MJ/OneDrive - Ulster University/' ...
        'Documents/PhD/Django/django-banter/ecg/media/results/%d.csv'];
    file_id = sprintf(path_dir,id); % output file ID is in the name
    csvwrite(file_id, dataOut);
    y = id;  % return function was successful
    
    %% Archived code
%     csvwrite(['C:\Users\MJ\OneDrive - Ulster University\' ...
%         'Documents\PhD\Django\django-banter\ecg\media\results\' ...
%         'LPF_single_row_result.csv'],dataOut);  % save to CSV file
end
