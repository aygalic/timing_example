#include <pybind11/pybind11.h>
#include <mpi.h>



#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int initialized, finalized, size, rank;


void mpi_init() {
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
}

void mpi_finalize() {
    MPI_Finalize();
}

int mpi_rank() {
    return rank;
}


int basic_operation(int i, int j) {
    int sum = 0;
    for(int l = 0; l < i; l++){
        sum = sum + j;

    }
    return sum;
}


int mpi_basic_operation(int i, int j){

    int local_sum = 0;
    int total = 0;

    for(int l = 0; l < floor(i/size+1); l++){
        local_sum = local_sum + j;
    }

    MPI_Reduce (&local_sum, &total, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    return total;


}







namespace py = pybind11;

PYBIND11_MODULE(timing_example, m) {

    m.def("basic_operation", &basic_operation, "sums a given number j a given amount of time i");

    m.def("mpi_basic_operation", &mpi_basic_operation, "sums in parallel a given number j a given amount of time i ");

    m.def("mpi_init", &mpi_init, "bind MPI_Init");

    m.def("mpi_finalize", &mpi_finalize, "bind MPI_Finalize");

    m.def("mpi_rank", &mpi_rank, "return the rank of the process");



#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
