/*
 * In this assignment you will implement one or more algorithms for the 2SAT
 * problem. Here are 6 different 2SAT instances: #1 #2 #3 #4 #5 #6.
 * The file format is as follows. In each instance, the number of variables and
 * the number of clauses is the same, and this number is specified on the first
 * line of the file. Each subsequent line specifies a clause via its two
 * literals, with a number denoting the variable and a "-" sign denoting logical
 * "not". For example, the second line of the first data file is "-16808 75250",
 * which indicates the clause ¬x16808∨x75250.
 *
 * Your task is to determine which of the 6 instances are satisfiable, and which
 * are unsatisfiable. In the box below, enter a 6-bit string, where the ith bit
 * should be 1 if the ith instance is satisfiable, and 0 otherwise. For example,
 * if you think that the first 3 instances are satisfiable and the last 3 are
 * not, then you should enter the string 111000 in the box below.
 *
 * DISCUSSION: This assignment is deliberately open-ended, and you can implement
 * whichever 2SAT algorithm you want. For example, 2SAT reduces to computing the
 * strongly connected components of a suitable graph (with two vertices per
 * variable and two directed edges per clause, you should think through the
 * details). This might be an especially attractive option for those of you who
 * coded up an SCC algorithm for my Algo 1 course. Alternatively, you can use
 * Papadimitriou's randomized local search algorithm. (The algorithm from
 * lecture is probably too slow as stated, so you might want to make one or more
 * simple modifications to it --- even if this means breaking the analysis given
 * in lecture --- to ensure that it runs in a reasonable amount of time.) A
 * third approach is via backtracking. In lecture we mentioned this approach
 * only in passing; see Chapter 9 of the Dasgupta-Papadimitriou-Vazirani book,
 * for example, for more details.
 */

#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>

using namespace std;

bool check_if_exists(int** clauses, int n, int variable) {
  for (int i = 0; i < n; ++i) {
    if (clauses[i][2] == 1 &&
        (clauses[i][0] == variable || clauses[i][1] == variable)) {
      return true;
    }
  }
  return false;
}

int remove_clauses(int** clauses, map<int, vector<int> >& vc, int variable) {
  int count = 0;
  for (vector<int>::iterator it = vc[variable].begin(); it != vc[variable].end(); ++it) {
    if (clauses[*it][2] == 1) {
      // remove other variable from all the clauses.
      int val = clauses[*it][0] == variable ? clauses[*it][1] : clauses[*it][0];
      // erase-remove idiom - this removes *it from vc[val].
      vc[val].erase(remove(vc[val].begin(), vc[val].end(), *it), vc[val].end());
      if (vc[val].size() == 0) {
        vc.erase(val);
      }
      // set clause as disabled.
      clauses[*it][2] = 0;
      ++count;
    }
  }
  // remove variable from vc.
  vc.erase(variable);
  return count;
}

void print_assignment(set<int>& rv, map<int, bool>& assignment) {
  set<int>::iterator it;
  for (it = rv.begin(); it != rv.end(); ++it) {
    cout << *it << "-" << assignment[*it] << endl;
  }
  cout << endl;
}

// returns -1 if assignment satisfies all the clauses. otherwise, returns the
// index of a randomly chosen unsatisfied clause.
int check_assignment(int** clauses, int n, map<int, bool>& assignment) {
  bool satisfied = true;
  vector<int> unsatisfied_clauses;
  for (int i = 0; i < n; ++i) {
    bool truth_value = false;
    for (int j = 0; j < 2; ++j) {
      int v = clauses[i][j];
      truth_value |= (v < 0) ? !assignment[abs(v)] : assignment[abs(v)];
    }
    if (!truth_value) {
      satisfied = false;
      unsatisfied_clauses.push_back(i);
    }
  }
  return satisfied ? -1 : unsatisfied_clauses[rand() % unsatisfied_clauses.size()];
}

void two_sat(string filename) {
  srand (time(NULL));
  cout << "filename: " << filename << endl;

  int n;
  ifstream in(filename.c_str());
  in >> n;
  cout << n << endl;

  // read the clauses
  int** clauses = new int*[n];
  map<int, vector<int> > variable_clauses;
  for (int i = 0; i < n; ++i) {
    clauses[i] = new int[3];
    in >> clauses[i][0] >> clauses[i][1];
    clauses[i][2] = 1;
    variable_clauses[clauses[i][0]].push_back(i);
    variable_clauses[clauses[i][1]].push_back(i);
  }

  // remove obvious clauses - if a variable only appears as a positive in all
  // clauses, then remove that clause from consideration, setting the variable
  // to True. vice versa for negative. repeatedly do this until no more clauses
  // can be removed.
  int removed_clauses;
  int global_removed_clauses = 0;
  do {
    removed_clauses = 0;
    for (int i = 0; i < n; ++i) {
      if (clauses[i][2] == 1) { // if clause is under consideration.
        for (int j = 0; j < 2; ++j) {
          int variable = clauses[i][j];
          // see if negation of variable is found in any of the clauses.
          bool negation_found =
            variable_clauses.find(-variable) != variable_clauses.end();
          if (!negation_found) {
            removed_clauses += remove_clauses(clauses, variable_clauses, variable);
            break;
          }
        }
      }
    }
    global_removed_clauses += removed_clauses;
  } while (removed_clauses != 0);

  cout << "total number of removed clauses: " << global_removed_clauses << endl;

  int new_n = n - global_removed_clauses;

  cout << "clauses left: " << new_n << endl;

  if (new_n == 0) {
    cout << "satisfied!" << endl;
    for (int i = 0; i < n; ++i) {
      delete[] clauses[i];
    }
    delete[] clauses;
    return;
  }

  int** remaining_clauses = new int*[new_n];
  for (int i = 0; i < new_n; ++i) {
    remaining_clauses[i] = new int[2];
  }

  set<int> rv;
  for (int i = 0, j = 0; i < n; ++i) {
    if (clauses[i][2] == 1) {
      remaining_clauses[j][0] = clauses[i][0];
      remaining_clauses[j][1] = clauses[i][1];
      rv.insert(abs(clauses[i][0]));
      rv.insert(abs(clauses[i][1]));
      ++j;
    }
  }

  set<int>::iterator it;
  map<int, bool> assignment;
  for (it = rv.begin(); it != rv.end(); ++it) {
    assignment[*it] = false;
  }

  int log_n = ceil(log2(rv.size()));
  int n_squared = 2 * rv.size() * rv.size();
  int k = 0;
  bool satisfied = false;
  while (k++ < log_n) {
    // generate a random initial assignment.
    for (it = rv.begin(); it != rv.end(); ++it) {
      assignment[*it] = (rand() % 2) ? true : false;
    }
    int j = 0;
    while (j++ < n_squared) {
      //print_assignment(rv, assignment);
      int rc = check_assignment(remaining_clauses, new_n, assignment);
      satisfied = (rc == -1);
      if (satisfied) {
        cout << "satisfied!" << endl;
        break;
      }
      // pick an unsatisfied clause in random and flip the value of its
      // variables.
      //cout << "picking clause " << rc << endl;
      int v1 = abs(remaining_clauses[rc][rand() % 2]);
      assignment[v1] = !assignment[v1];
      //cout << "flipping assignment for variable " << v1 << endl;
    }
    if (satisfied) {
      break;
    }
  }

  cout << "satisfied? " << satisfied << endl;

  // delete stuff
  for (int i = 0; i < n; ++i) {
    delete[] clauses[i];
  }
  delete[] clauses;
  for (int i = 0; i < new_n; ++i) {
    delete[] remaining_clauses[i];
  }
  delete[] remaining_clauses;

  cout << "=========" << endl << endl;
}

int main(void) {
  two_sat("2sat1.txt");
  two_sat("2sat2.txt");
  two_sat("2sat3.txt");
  two_sat("2sat4.txt");
  two_sat("2sat5.txt");
  two_sat("2sat6.txt");
  return 0;
}
