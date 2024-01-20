#include <stdio.h>
#define SIZE 100

// adjacency matrix
int adj[SIZE][SIZE] = {0};
// visited array
int visited[SIZE] = {0};

void DFS(int v, int n) {
    visited[v] = 1;
    printf("%d ", v);
    for(int i = 0; i < n; i++) {
        if(adj[v][i] == 1 && visited[i] == 0) {
            DFS(i, n);
        }
    }
}

int main() {
    int nodes, edges, x, y;

    printf("Enter number of nodes and edges: ");
    scanf("%d%d", &nodes, &edges);

    for(int i = 0; i < edges; i++) {
        printf("Enter edge (u, v): ");
        scanf("%d%d", &x, &y);
        adj[x][y] = 1;
        adj[y][x] = 1; // for undirected graph
    }

    printf("DFS traversal: ");
    DFS(0, nodes);

    return 0;
}
