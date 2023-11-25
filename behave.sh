#!/bin/sh

test_feature() {
    behave $1 $2 $3
    TESTS_EXIT_VALUE=$?
    if [ $TESTS_EXIT_VALUE != 0 ]
    then
        exit $TESTS_EXIT_VALUE
    fi
}


main(){
    test_feature "tests/behave/version/features/" $1 $2
    test_feature "tests/behave/login/features/" $1 $2
    test_feature "tests/behave/finanzas/features/" $1 $2
}

main $1 $2
