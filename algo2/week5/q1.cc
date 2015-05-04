/*
 * In this assignment you will implement one or more algorithms for the
 * traveling salesman problem, such as the dynamic programming algorithm covered
 * in the video lectures. Here is a data file describing a TSP instance. The
 * first line indicates the number of cities. Each city is a point in the plane,
 * and each subsequent line indicates the x- and y-coordinates of a single city.
 * The distance between two cities is defined as the Euclidean distance.
 *
 * In the box below, type in the minimum cost of a traveling salesman tour for
 * this instance, rounded down to the nearest integer.
 *
 * OPTIONAL: If you want bigger data sets to play with, check out the TSP
 * instances from around the world here. The smallest data set (Western Sahara)
 * has 29 cities, and most of the data sets are much bigger than that. What's
 * the largest of these data sets that you're able to solve --- using dynamic
 * programming or, if you like, a completely different method?
 *
 * HINT: You might experiment with ways to reduce the data set size. For
 * example, trying plotting the points. Can you infer any structure of the
 * optimal solution? Can you use that structure to speed up your algorithm?
 */

// This takes about 3 minutes in my Macbook Air.

#include <iostream>
#include <fstream>
#include <cfloat>
#include <cmath>

using namespace std;

double MAX = 10000000000.0;

double dist(double** G, int i, int j) {
  double p0 = pow(G[i][0] - G[j][0], 2);
  double p1 = pow(G[i][1] - G[j][1], 2);
  return sqrt(p0 + p1);
}

bool contains(int x, int position) {
  return (x & (1 << position)) != 0;
}

int remove(int x, int position) {
  return x & (~(1 << position));
}

string binary(int x) {
  return bitset<8>(x).to_string();
}

void tsp(string filename) {
  int n;
  ifstream in(filename.c_str());
  in >> n;
  cout << n << endl;

  // read the input graph. stored as a nx2 array representing x,y
  double** G = new double*[n];
  for (int i = 0; i < n; ++i) {
    G[i] = new double[2];
    in >> G[i][0] >> G[i][1];
  }
 
  // size of 2d array A is 2^n x n
  long two_power_n = (1 << n);
  double** A = new double*[two_power_n];
  for (long i = 0; i < two_power_n; ++i) {
    A[i] = new double[n];
  }

  // base case
  for (long i = 0; i < two_power_n; ++i) {
    A[i][0] = (i == 1) ? 0 : MAX;
  }

  // main loop
  for (int m = 2; m < n + 1; ++m) {
    // m represents the sub-problem size. using gosper's hack, we generate all
    // sets of size m and do the recurrence for each of those.
    int set = (1 << m) - 1;
    int limit = (1 << n);
    while (set < limit) {
      if (!contains(set, 0)) {
        // if the set does not contain element 0, then ignore.
      } else {
        for (int j = 1; j < n; ++j) {
          if (contains(set, j)) {
            double min = MAX;
            int s_minus_j = remove(set, j);
            for (int k = 0; k < n; ++k) {
              if (k == j || !contains(set, k)) {
                continue;
              }
              double value = A[s_minus_j][k] + dist(G, k, j);
              if (value < min) {
                min = value;
              }
            }
            A[set][j] = min;
          }
        }
      }
      // Gosper's hack to generate the next set of size m
      int c = set & -set;
      int r = set + c;
      set = (((r ^ set) >> 2) / c) | r;
    }
  }

  double min = MAX;
  // compute last hop minimum.
  for (int j = 1; j < n; ++j) {
    double value = A[two_power_n - 1][j] + dist(G, j, 0);
    if (value < min) {
      min = value;
    }
  }
  cout << "Optimal TSP cost: " << min << endl;

  // delete G
  for (int i = 0; i < n; ++i) {
    delete[] G[i];
  }
  delete[] G;

  // delete A
  for (long i = 0; i < two_power_n; ++i) {
    delete[] A[i];
  }
  delete[] A;
}

int main(void) {
  tsp("tsp.txt");
  return 0;
}
