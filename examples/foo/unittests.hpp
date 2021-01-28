#ifndef UNITTESTS_HPP
#define UNITTESTS_HPP


namespace unittests{

struct test_results{

    enum status{ ok, fail, error };

    void update( const char* test_name, status result );
};

struct test_case{

    test_case( const char* test_case_name );

    virtual void set_up(){}

    virtual void tear_down(){}

    virtual void run() = 0;

private:
    const char* m_name;
};

class test_container;

struct test_suite : public test_case{

    test_suite();

    void run();

    const test_results& get_results() const
    { return m_results; }

private:
    test_container* m_tests;
    test_results m_results;
};

}

#endif //UNITTESTS_HPP