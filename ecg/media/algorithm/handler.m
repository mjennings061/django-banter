function y = handler(script_file_path, data_file_path)
    fclose('all');
    % Sanitise both args (regex)
    addpath('C:\Users\MJ\OneDrive - Ulster University\Documents\PhD\Django\django-banter\ecg\media\algorithm');
    [script_path,script_name,script_ext] = fileparts(script_file_path);
    func_to_exec = str2func(script_name);
    y = func_to_exec(data_file_path);
end