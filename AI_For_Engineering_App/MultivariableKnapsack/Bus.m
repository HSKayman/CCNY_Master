
clc;
clear;

% set up money_to_spend and gasoline_consumption:

money_to_spend = 2500;
gasoline_consumption = 60;

% read input file into bus_table:

input_file = "Bus_info.csv";
bus_table = readtable(input_file);

% define chromosome length and fitness function:
chromosome_length = height(bus_table);
fit_func= @(chromosome) - (chromosome * bus_table.Passengers);

% define masks based on bus_table:
category_index_map = containers.Map();

for i=1:height(bus_table)
    category = string(bus_table.Companies(i));
    if isKey(category_index_map,category)
        indices = category_index_map(category);
        category_index_map(category) = [indices,i];
    else
        category_index_map(category) = [i];
    end
end

noof_categories = size(category_index_map,1);
masks = zeros(noof_categories,height(bus_table));
keySet = keys(category_index_map);

for i = 1:noof_categories
    indices = category_index_map(keySet{i});
    for j = 1:length(indices)
        masks(i,indices(j)) =1;
    end
end

%set A, b, Lb, Ub, int_indices:

A= [bus_table.Costs';bus_table.Gasoline'];
A= [A;masks];
b= [ money_to_spend,gasoline_consumption,ones(1,noof_categories)];
Lb = zeros(1,chromosome_length);
Ub = ones(1,chromosome_length);
int_indices = 1:chromosome_length;

% run ga:
disp('****GA STARTING*****');
options = optimoptions('ga','display','off');
selection = ga(fit_func,chromosome_length,A,b,...
[],[],Lb,Ub,[],int_indices);
disp('****GA Finished****');

if isempty(selection)
    message = sprintf('GA CANNOT FIND VALID SELECTION WITH GIVEN CONSTRAINTS');
    disp(message)
    return
end

% display results:
message = sprintf('OPTIMAL SELECTION OF ITEMS: [');
for i = 1:chromosome_length
    if selection(i) == 1
            message = sprintf('%s \n\t %s - %s', message, ... 
                string(bus_table.Companies(i)), string(bus_table.Type(i)));
    end
end
fprintf('%s \n]\n', message);
fprintf('TOTAL PASSENGERS: %d\n', selection * bus_table.Passengers);
fprintf('TOTAL MONEY SPENT: $%dM\n', selection * bus_table.Costs);
fprintf('TOTAL GAS USED: %dK GALLONS\n', selection * bus_table.Gasoline);
disp('*********************************************')

