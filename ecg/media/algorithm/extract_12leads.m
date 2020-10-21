function y = extract_12leads(filePath)
    %% Import data
    fclose('all');
    data = importdata(filePath); % read from a MAT file
    
    %% Function-execution
    realLead{1, length(data)} = [];
    for n = 1:length(data)  %for all patients
        [nNodes, N] = size(data{n}); %this will need to change with different patients

        %% Extract real lead data
         %One matrix for all leads wrt time
        %         time (t) -->-->
        % lead I [n n-1 n-2 ... n-N]
        % lead II[n n-1 n-2 ... n-N]
        % ...
        % lead V6[n n-1 n-2 ... n-N]
        realLead{n} = zeros(8,N);      %row = lead I to V6. col = samples(1:N)
        realLead{n}(1,:) = data{n}(2,:); %I
        realLead{n}(2,:) = data{n}(3,:); %II
        realLead{n}(3,:) = data{n}(172,:); %V1
        realLead{n}(4,:) = data{n}(174,:); %V2
        realLead{n}(5,:) = (data{n}(195,:) + data{n}(196,:))/2; %V3
        realLead{n}(6,:) = data{n}(219,:); %V4
        realLead{n}(7,:) = (data{n}(220,:) + 2*data{n}(221,:))/3; %V5
        realLead{n}(8,:) = data{n}(222,:); %V6
    end
    dataOut = realLead;
    
    %% Django-specific operations
    rng('shuffle');     % to help prevent the same 'random number'
    id = randi(2^32);   % generate a random number as the file ID
    path_dir = ['C:/Users/MJ/OneDrive - Ulster University/' ...
        'Documents/PhD/Django/django-banter/ecg/media/results/%d.mat'];
    file_id = sprintf(path_dir,id); % output file ID is in the name
    save(file_id, 'dataOut');
    y = id;  % return function was successful
end