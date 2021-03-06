# pact-k6-demo

This is a very quick demo application to get both Pact and K6 running against a simple Python web service in order to demonstrate Contract Testing via PACT and a simple performance set up with K6. Both can be executed with and without `Docker` so the usage is up to you. If you wish to trial the `PACT Broker` you will need to use Docker.

Note - if you are using MacOS, you probably don't want to use the default Python installation - [this then instead](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)

TODO: K6 instructions still need added :-)

## General Setup
You will have to have Python installed on your machine. To get started, install all the required Python dependencies

```
pip install Pipfile
```

## Without Broker
Running without Docker will mean that you cannot make use of the PACT Broker in this demo - though it is not pre-requisite in general as the Broker can be launched in many ways, Docker makes it a convenience. Nonetheless, to get going:

Run the initial tests with `Pytest`, this will create a contract from the PACT written unit tests (Explore the `tests\test_consumer.py` file for understanding how these are structured):

```
pytest
```

The unit tests should complete and you'll note that a pact contract is generated in the `tests` folder:

```
pytest
===================================================================================================================== test session starts =====================================================================================================================
platform darwin -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /Users/neill/non-payroc-dev/pact-k6-demo
collected 2 items

tests/test_consumer.py ..                                                                                                                                                                                                                               [100%]

===================================================================================================================== 2 passed in 13.54s ======================================================================================================================
neill@Neills-MacBook-Pro pact-k6-demo %
```

The pact file will be:

```
tests\userserviceclient-userservice.json
```

This will be the contract that we validate the `provider` against. To do that:

```
python demo/provider.py
pact-verifier --provider-base-url=http://localhost:5001 --pact-url=tests/userserviceclient-userservice.json --provider-states-setup-url=http://localhost:5001/_pact/provider_states
```

The `pact-verifier` command needs the url of the provider service, the location of the pact contract and the provider states set up information for testing. Upon successful completion, the provider should be validated against the consumer contract:

```
Verifying a pact between UserServiceClient and UserService
  Given UserA exists and is not an administrator
    a request for UserA
      with GET /users/UserA
        returns a response which
          has status code 200
          has a matching body
  Given UserA does not exist
    a request for UserA
      with GET /users/UserA
        returns a response which
          has status code 404

2 interactions, 0 failures
```

If the `provider` was to change any of it's implementation details without a new contract established, this check will fail and ultimately provide information to the teams that this will break a dependent service's workflow.


## With the Broker (Needs Docker)
To execute with a broker - we'll start the broker via Docker Compose:

```
cd broker
docker-compose up
```

You can now access the broker on your localhost with a username of `pactbroker` and a password of `pactbroker`. The remaining steps are similar - be sure to explore the broker service as you execute each step so you can see how it fits, it essentially acts as a storage for all of your contracts and what version of a service they relate to.

To create the contract and send it to the broker:

```
pytest --publish-pact 0.1
```

This will again run the unit tests and generate the PACT contract and publish it to the broker as `Version 0.1` of the `Consumer Service` - you can check this out on the broker UI.

To validate your provider against this, use the bash script included (and take a look at it!):

```
python demo/provider.py
./verify_pact.sh 0.2
```

This will execute the verification script against a hypothetical `Version 0.2` of the provider against the consumer pact 0.1 - play around with the services and make various changes to see the impact.
