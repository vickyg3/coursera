// see q1.py for the question

#include <iostream>
#include <fstream>
#include <climits>

using namespace std;

bool check_cycle(int*** A, int n, int n_index) {
  for (int i = 1; i < n + 1; ++i) {
    if (A[n_index][i][i] < 0) {
      return true;
    }
  }
  return false;
}

void floyd_warshall(string filename) {
  int m, n;
  ifstream in(filename.c_str());
  in >> m >> n;
  cout << filename << endl;
  int** G = new int*[n + 1];
  for (int i = 1; i < n + 1; ++i) {
    G[i] = new int[n + 1];
    for (int j = 1; j < n + 1; ++j) {
      G[i][j] = INT_MAX;
    }
  }
  while (!in.eof()) {
    int src, dst, cost;
    in >> src >> dst >> cost;
    G[src][dst] = cost;
  }
  // allocate the 2*n*n array
  int*** A = new int**[2];
  for (int k = 0; k < 2; ++k) {
    A[k] = new int*[n + 1];
    for (int i = 1; i < n + 1; ++i) {
      A[k][i] = new int[n + 1];
    }
  }
  // base case
  for (int i = 1; i < n + 1; ++i) {
    for (int j = 1; j < n + 1; ++j) {
      A[0][i][j] = (i == j) ? 0 : G[i][j];
    }
  }
  // delete G
  for (int i = 1; i < n + 1; ++i) {
    delete[] G[i];
  }
  delete[] G;
  // floyd warshall loop
  int curr_k, prev_k;
  for (int k = 1; k < n + 1; ++k) {
    curr_k = k % 2;
    prev_k = (k - 1) % 2;
    for (int i = 1; i < n + 1; ++i) {
      for (int j = 1; j < n + 1; ++j) {
        // prevent overflows in case 2
        if (A[prev_k][i][k] == INT_MAX || A[prev_k][k][j] == INT_MAX) {
          A[curr_k][i][j] = A[prev_k][i][j];
          continue;
        }
        int c1 = A[prev_k][i][j]; // case 1
        int c2 = A[prev_k][i][k] + A[prev_k][k][j]; // case 2
        A[curr_k][i][j] = (c1 < c2) ? c1 : c2;
      }
    }
    if (check_cycle(A, n, curr_k)) {
      break;
    }
  }
  bool negative_cycle = check_cycle(A, n, curr_k);
  cout << "negative cycle: " << negative_cycle << endl;
  // compute the shortest shortest path if there are no negative cycles
  if (!negative_cycle) {
    int shortest = INT_MAX;
    for (int i = 1; i < n + 1; ++i) {
      for (int j = 1; j < n + 1; ++j) {
        if (A[curr_k][i][j] < shortest) {
          shortest = A[curr_k][i][j];
        }
      }
    }
    cout << "shortest: " << shortest << endl;
  }
  for (int k = 0; k < 2; ++k) {
    for (int i = 1; i < n + 1; ++i) {
      delete[] A[k][i];
    }
    delete[] A[k];
  }
  delete[] A;
  cout << "done :)" << endl;
}

int main(void) {
  floyd_warshall("simple1.txt");
  floyd_warshall("simple2.txt");
  floyd_warshall("simple3.txt");
  floyd_warshall("g1.txt");
  floyd_warshall("g2.txt");
  floyd_warshall("g3.txt");
  return 0;
}
