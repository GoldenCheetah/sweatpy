import vcr

sweatvcr = vcr.VCR(cassette_library_dir="tests/fixtures/cassettes",)
