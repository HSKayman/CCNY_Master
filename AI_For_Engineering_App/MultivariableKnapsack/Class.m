
clc;
clear;

% set budget, and read input file into class_table:

input_file = 'Class_info.csv';
class_table =  readtable(input_file);
class_table = sortrows(class_table,'ClassType');
budget = 2500;

% Define limits for each class type:
classTypes = {'EE','ELECTIVE','ENGR','LIBERAL'};
classLimits = [2,1,1,0]; % number of each classType allowed (i.e., max)
classTypes = sortrows(classTypes);
classMap = containers.Map(classTypes,classLimits);

% define chromosome and fitness function:

chromosome_length = height(class_table);
fit_func= @(chromosome) - (chromosome * class_table.Credits);

% defined masks based on class_table:
masks = zeros(width(classLimits),height(class_table));
for i=1: width(classLimits)
    for j=1: height(class_table)
        if strcmp(classTypes(i),string(class_table.ClassType(j)))
            masks(i,j)=1;
        else
            masks(i,j)=0;
        end
    end
end
% define A, b, Lb, Ub, and int_indices:

A = vertcat(class_table.Costs', masks);
b = [budget, classLimits];
Lb = zeros(1,chromosome_length);
Ub = ones(1,chromosome_length);
int_indices = 1:chromosome_length;

% run ga:
disp('****GA STARTING*****');
options = optimoptions('ga','display','diagnose');
selection = ga(fit_func,chromosome_length,A,b,...
[],[],Lb,Ub,[],int_indices);
disp('****GA Finished****');

% display results:
message = sprintf('OPTIMAL SELECTION OF ITEMS: [');
for i = 1:chromosome_length
    if selection(i) == 1
        message = sprintf('%s \n\t%s - %s', message, string(class_table.Class(i)), ...
            string(class_table.Class_Name(i)));    
    end
end

fprintf('%s \n]\n', message);
fprintf('TOTAL CREDITS TO TAKE THIS SEMESTER: %d\n', selection * class_table.Credits);
fprintf('TOTAL TUITION FOR THIS SEMESTER: $%d\n', selection * class_table.Cost);
disp('*********************************************')
