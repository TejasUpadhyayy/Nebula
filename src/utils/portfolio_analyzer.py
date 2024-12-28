class PortfolioAnalyzer:
    def __init__(self):
        self.portfolio = {}
    
    def add_stock(self, symbol, shares, purchase_price):
        """Add stock to portfolio"""
        self.portfolio[symbol] = {
            'shares': shares,
            'purchase_price': purchase_price
        }
    
    def analyze_portfolio(self, current_prices, predictions):
        """Analyze entire portfolio"""
        analysis = {
            'total_value': 0,
            'total_cost': 0,
            'potential_value': 0,
            'stocks': {}
        }
        
        for symbol in self.portfolio:
            stock = self.portfolio[symbol]
            current_price = current_prices[symbol]
            predicted_price = predictions[symbol]
            
            stock_analysis = {
                'current_value': stock['shares'] * current_price,
                'cost_basis': stock['shares'] * stock['purchase_price'],
                'potential_value': stock['shares'] * predicted_price,
                'profit_loss': stock['shares'] * (current_price - stock['purchase_price']),
                'predicted_change': (predicted_price - current_price) / current_price * 100
            }
            
            analysis['stocks'][symbol] = stock_analysis
            analysis['total_value'] += stock_analysis['current_value']
            analysis['total_cost'] += stock_analysis['cost_basis']
            analysis['potential_value'] += stock_analysis['potential_value']
            
        return analysis