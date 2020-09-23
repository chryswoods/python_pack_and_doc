
#define omp_lock_t int

inline void omp_set_lock(omp_lock_t *lock)
{}

inline void omp_unset_lock(omp_lock_t *lock)
{}

inline void omp_init_lock(omp_lock_t *lock)
{}
