except asyncio.exceptions.TimeoutError:
        logger.warning(f"{COLOR_RED}Timeout occurred - returning failure response{COLOR_RESET}")

        global timeout_failures, total_requests
        timeout_failures += 1
        failure_rate = 100.0 * timeout_failures / total_requests
        logger.warning(f"Current timeout failure rate: {failure_rate:.2f}%")

        return ServerResponse(
            valid=False,
            ttft_ms=-1.0,
            tpot_ms=-1.0,
            latency_ms=-1.0,
            start_time_ms=time.perf_counter_ns() / 1e6,
            first_chunk="",
            content="[TIMEOUT_FAKE_RESPONSE]",
            num_chunks=0,
        )

    except Exception as e:
        logger.exception(f"{COLOR_RED}Unexpected exception: {e}{COLOR_RESET}")
        return ServerResponse(
            valid=False,
            ttft_ms=-1.0,
            tpot_ms=-1.0,
            latency_ms=-1.0,
            start_time_ms=time.perf_counter_ns() / 1e6,
            first_chunk="",
            content="[EXCEPTION_FAKE_RESPONSE]",
            num_chunks=0,
        )