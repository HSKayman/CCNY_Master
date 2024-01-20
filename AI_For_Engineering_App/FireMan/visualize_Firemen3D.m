
%% Visualizing the results
function visualize_Firemen3D(firemen_positions, num_moves, firefighters, dist_fire)
    figure;

    [unit_sph_x, unit_sph_y, unit_sph_z] = sphere; 
    
    min_x = min(min(firemen_positions(:,1,:))) - dist_fire;
    max_x = max(max(firemen_positions(:,1,:))) + dist_fire;
    min_y = min(min(firemen_positions(:,2,:))) - dist_fire;
    max_y = max(max(firemen_positions(:,2,:))) + dist_fire;
    min_z = 0;
    max_z = max(max(firemen_positions(:,3,:))) + dist_fire;
    x_span = (max_x - min_x);
    y_span = (max_y - min_y);
    x_axis_min = (round(min_x/dist_fire)-1)*dist_fire;
    x_axis_max = (round(max_x/dist_fire)+1)*dist_fire;
    y_axis_min = (round(min_y/dist_fire)-1)*dist_fire;
    y_axis_max = (round(max_y/dist_fire)+1)*dist_fire;
    z_axis_min = min_z;
    z_axis_max = (round(max_z/dist_fire)+1)*dist_fire;
    
    for t = 1:num_moves
       pause(0.25); 
       hold off

       for fire_num = 1:firefighters
            x_pos = firemen_positions(fire_num,1,t);
            y_pos = firemen_positions(fire_num,2,t);
            z_pos = firemen_positions(fire_num,3,t);

            sph_x = (dist_fire*unit_sph_x + x_pos);
            sph_y = (dist_fire*unit_sph_y + y_pos);
            sph_z = (dist_fire*unit_sph_z + z_pos);
            surf(sph_x, sph_y, sph_z,'FaceColor', 'blue', ...
                 'LineStyle', '-', 'EdgeColor', 'blue', ... 
                 'FaceAlpha', 0.05, 'EdgeAlpha', 0.1);
            xlim([x_axis_min x_axis_max])
            ylim([y_axis_min y_axis_max])
            zlim([z_axis_min z_axis_max])
            hold on
            
            scatter3(x_pos, y_pos, z_pos, 'filled');
       end
       % visualize 10 floors of the building 
       for i = 0:10:100
           patch([x_axis_max x_axis_min x_axis_min x_axis_max], ...
                    [y_axis_max y_axis_max y_axis_min y_axis_min], [i i i i], ...
                    [186 186 186]./255, 'FaceAlpha', 0.2, 'EdgeColor', [0 0 0], ...
                    'EdgeAlpha', 1);
           hold on
       end
       plot_title = sprintf('Firemen Positions at t = %d', t);
       title(plot_title);
       box on
       xlim([x_axis_min x_axis_max]);
       ylim([y_axis_min y_axis_max]);
    end
end