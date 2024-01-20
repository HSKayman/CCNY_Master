#include <stdio.h>
#define N 1000
#define M 2000

typedef struct Edge {
    int u, v, w;
} Edge;

typedef struct Graph {
    int n, m;
    Edge edges[M];
} Graph;

int parent[N];

void make_set(int v) {
    parent[v] = v;
}

int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b)
        parent[b] = a;
}

void boruvkaMST(Graph* g) {
    int weight = 0;
    Edge result[g->n];
    int num_edges = 0;
    for (int i = 0; i < g->n; i++)
        make_set(i);
    while (num_edges < g->n - 1) {
        int min_e[g->n];
        for (int i = 0; i < g->n; i++)
            min_e[i] = -1;
        for (int i = 0; i < g->m; i++) {
            int u = find_set(g->edges[i].u);
            int v = find_set(g->edges[i].v);
            if (u != v) {
                if (min_e[u] == -1 || g->edges[i].w < g->edges[min_e[u]].w)
                    min_e[u] = i;
                if (min_e[v] == -1 || g->edges[i].w < g->edges[min_e[v]].w)
                    min_e[v] = i;
            }
        }
        for (int i = 0; i < g->n; i++) {
            if (min_e[i] != -1) {
                int u = g->edges[min_e[i]].u;
                int v = g->edges[min_e[i]].v;
                int w = g->edges[min_e[i]].w;
                if (find_set(u) != find_set(v)) {
                    weight += w;
                    result[num_edges++] = g->edges[min_e[i]];
                    union_sets(u, v);
                }
            }
        }
    }
    printf("Edges in the minimum spanning tree:\n");
    for (int i = 0; i < num_edges; i++)
        printf("%d -- %d == %d\n", result[i].u, result[i].v, result[i].w);
    printf("Total weight of the minimum spanning tree: %d\n", weight);
}

int main() {
    Graph g = {4, 5, {{0, 1, 10}, {0, 2, 6}, {0, 3, 5}, {1, 3, 15}, {2, 3, 4}}};
    boruvkaMST(&g);
    return 0;
}
