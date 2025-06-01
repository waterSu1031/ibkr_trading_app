def check_sufficient_funds(self) -> bool:
    """Check if account has sufficient funds (50% reserve)"""
    try:
        # Explicitly type the account_summary
        account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []

        for summary in account_summary:
            if summary.tag == "NetLiquidation":
                total_funds = float(summary.value)
                # Ensure we keep 50% in reserve
                return total_funds * 0.5 >= 0
        return False

    except Exception as e:
        raise OrderException(f"Failed to check funds: {str(e)}")


def get_available_funds(self) -> Optional[float]:
    """Get available funds for _web_app"""
    try:
        # Explicitly type the account_summary
        account_summary: List[AccountValue] = self.ib.reqAccountSummary() or []

        for summary in account_summary:
            if summary.tag == "NetLiquidation":
                total_funds = float(summary.value)
                return total_funds * 0.5  # Return available funds (50% of total)
        return None

    except Exception as e:
        raise OrderException(f"Failed to get available funds: {str(e)}")


def get_positions(self) -> Dict[str, float]:
    """Get current positions"""
    try:
        positions: Dict[str, float] = {}
        for position in self.ib.positions() or []:
            symbol = position.contract.symbol
            quantity = position.position
            positions[symbol] = quantity
        return positions

    except Exception as e:
        raise OrderException(f"Failed to get positions: {str(e)}")


    def send_report(self) -> None:
        try:
            paths = self.reporter.generate_report()
            recv = os.getenv("TRADING_REPORT_EMAIL")
            if recv:
                summary = {
                    "open_positions": self.positions,
                    "timestamp": self.trading_hours.current_timestamp()
                }
                self.emailer.send_report(recv, paths, summary)
            else:
                self.logger.info("No report email configured - skipping.")
        except Exception as e:
            self.logger.error(f"Report error: {e}")