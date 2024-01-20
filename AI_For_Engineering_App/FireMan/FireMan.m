%% Firemen Protection System Assignment 
clc 
clear
%% User inputs and initalizations
%user inputs:
firefighters = 16;
speed = 3; 
dist_fire = 10; 
num_moves = 22;

firemen_positions = zeros(firefighters, 3, num_moves); 
firemen_positions(:,:,1) = (dist_fire/sqrt(2)).*rand(firefighters, 3);
firemen_positions(:,3,1) = firemen_positions(:,3,1)+dist_fire;

% initialize the displacement vectors:
displacement_vectors = [[0, 1]; [1/sqrt(2.0), 1/sqrt(2.0)]; ...
                        [1, 0]; [1/sqrt(2.0), -1/sqrt(2.0)]; ...
                        [0, -1]; [-1/sqrt(2.0), -1/sqrt(2.0)];... 
                        [-1, 0]; [-1/sqrt(2.0), 1/sqrt(2.0)]];
           
displacement_vectors = speed.* displacement_vectors;

% Define the chromosome length:
chromosome_length = 5;

% Define the upper and lower bounds for the chromosomes:
Lb = zeros(1,chromosome_length);
Ub = ones(1,chromosome_length);

% Define indices of the chromosome which are integers:
int_indices = 1:chromosome_length;
options = optimoptions('ga','display','off'); 
for t = 1:num_moves-1
    fprintf("\n\n***** TIME IS NOW: %d*****\n", t)
   
    for fire_num = 1:firefighters
        fprintf("***** BEGINNING GA FOR FIREMEN #%d *****\n", fire_num)
        % get the neighbors and the current UAV's position
        % make sure the variable name is neighbors and current_position
        neighbors = firemen_positions(:,:,t);
        neighbors(fire_num,:) = [];
        current_position = firemen_positions(fire_num,:,t);
        % the fitness function - complete the fitness function definition
        % at the end of the script (second to last function)
        fit_func = @(chromosome) fitness_function(chromosome, ...
                   current_position, speed, neighbors, dist_fire, displacement_vectors);
        
        % run the genetic algorithm:
        selection = ga(fit_func,chromosome_length,[],[],...
                                    [],[],Lb,Ub,[],int_indices,options);
        % based on the selection from ga, determine the next position:
        displacement = displacement_vectors(bi2de(selection(3:end),'left-msb')+1,:);
        % assign the position for the next time step:
        next_position = get_next_position(selection,current_position, speed ,displacement_vectors);
        firemen_positions(fire_num,:,t+1) = next_position;
        % print the time stamp:position for the next time step:
        fprintf("***** FINISHED GA FOR FIREMEN #%d AT TIME %d *****\n", ...
            fire_num, t)
    end
end

%% Visualize the Firemen Path
visualize_Firemen3D(firemen_positions, num_moves, firefighters, dist_fire);
open_anim = true;
while open_anim == true
    fprintf("Would you like to replay the animation?\n\t(1) yes\n\t(2) no\n");
    user_choice = input('');
    if user_choice == 2
        open_anim = false;
        fprintf('Thank you. Have a nice day!\n');
        break;
    else
        close all
        visualize_Firemen3D(firemen_positions, num_moves, firefighters, dist_fire);
    end
end

%% functions
function fitness_score = fitness_function(chromosome, position, speed, ...
                            neighbors, dist_fire, displacement_vectors)
    % Write the fitness function here:
    fitness_score =0;
    neighbors_count = 0;
    candidate_pos = get_next_position(chromosome,position,speed,displacement_vectors);
    for i=1:length(neighbors)
        distance = norm(candidate_pos - neighbors(i,:));
        if distance <= dist_fire
            neighbors_count = neighbors_count +1;
            fitness_score = fitness_score + (dist_fire -distance);
        end
    end

    if neighbors_count<1 || candidate_pos(3) <= dist_fire
        fitness_score = abs(intmax);
    end
    %fitness_score = -1* fitness_score;
end


function next_pos = get_next_position(chromosome, position, speed, ...
                                        displacement_vectors)
    if bi2de(chromosome(1:2)) == 0 
         
        next_pos = position;
    elseif bi2de(chromosome(1:2), 'left-msb') == 1 
       
        displacement = displacement_vectors(bi2de(chromosome(3:end), 'left-msb')+1,:);
        next_pos(1:2)= position(1:2) + displacement;
        next_pos(3) = position(3) + speed; 
    elseif bi2de(chromosome(1:2), 'left-msb') == 2
      
        displacement = displacement_vectors(bi2de(chromosome(3:end), 'left-msb')+1,:);
        next_pos(1:2)= position(1:2) + displacement;
        next_pos(3) = position(3) - speed; 
    elseif bi2de(chromosome(1:2), 'left-msb') == 3 
       
        next_pos = position;
        displacement = displacement_vectors(bi2de(chromosome(3:end), 'left-msb')+1,:);
        next_pos(1:2)= position(1:2) + displacement;
    else
    end
end
