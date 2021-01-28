namespace ns {

struct B {
  struct D { bool d; };
};
struct D {};

template <typename T1, typename T2>
struct T {};

T<B::D, bool> function();

}