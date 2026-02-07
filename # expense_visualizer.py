# expense_visualizer.py
import os
import json
from datetime import datetime
import random

class ExpenseVisualizer:
    def __init__(self):
        self.expenses = []
        self.categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Education", "Other"]
        self.colors = {
            "Food": "\033[92m",  # Green
            "Transport": "\033[94m",  # Blue
            "Entertainment": "\033[95m",  # Magenta
            "Shopping": "\033[93m",  # Yellow
            "Bills": "\033[91m",  # Red
            "Health": "\033[96m",  # Cyan
            "Education": "\033[97m",  # White
            "Other": "\033[90m"  # Gray
        }
        self.reset_color = "\033[0m"
        self.data_file = "expenses.json"
        self.load_data()
    
    def load_data(self):
        """Load saved expenses from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.expenses = json.load(f)
            print(f"📂 Loaded {len(self.expenses)} expenses from file")
    
    def save_data(self):
        """Save expenses to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def add_expense(self):
        """Add a new expense"""
        print("\n" + "="*40)
        print("➕ ADD NEW EXPENSE")
        print("="*40)
        
        # Get amount
        while True:
            try:
                amount = float(input("💰 Amount: $"))
                if amount <= 0:
                    print("❌ Amount must be positive!")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number!")
        
        # Get category
        print("\n📁 Categories:")
        for i, cat in enumerate(self.categories, 1):
            print(f"  {i}. {cat}")
        
        while True:
            try:
                cat_choice = int(input(f"\nChoose category (1-{len(self.categories)}): "))
                if 1 <= cat_choice <= len(self.categories):
                    category = self.categories[cat_choice - 1]
                    break
                else:
                    print(f"❌ Please choose 1-{len(self.categories)}")
            except ValueError:
                print("❌ Please enter a number!")
        
        # Get description
        description = input("📝 Description: ").strip()
        if not description:
            description = f"{category} expense"
        
        # Add expense
        expense = {
            "id": len(self.expenses) + 1,
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "color": self.colors.get(category, "")
        }
        
        self.expenses.append(expense)
        self.save_data()
        
        print(f"\n✅ Expense added: ${amount:.2f} for {description}")
    
    def show_ascii_chart(self):
        """Display expenses as ASCII chart"""
        if not self.expenses:
            print("\n📭 No expenses to show!")
            return
        
        print("\n" + "="*50)
        print("📊 EXPENSE VISUALIZATION")
        print("="*50)
        
        # Group by category
        category_totals = {}
        for expense in self.expenses:
            cat = expense["category"]
            category_totals[cat] = category_totals.get(cat, 0) + expense["amount"]
        
        # Find max for scaling
        max_amount = max(category_totals.values()) if category_totals else 0
        
        print(f"\n📅 Total Expenses: ${sum(category_totals.values()):.2f}")
        print(f"📈 Number of entries: {len(self.expenses)}")
        print("-"*50)
        
        # Display chart
        for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (total / sum(category_totals.values())) * 100 if sum(category_totals.values()) > 0 else 0
            
            # Create bars (each █ = $20 or scaled)
            bar_length = int((total / max_amount) * 30) if max_amount > 0 else 0
            bars = "█" * bar_length
            
            color = self.colors.get(category, "")
            
            print(f"{color}{category:15} {bars} ${total:8.2f} ({percentage:5.1f}%){self.reset_color}")
    
    def show_spending_patterns(self):
        """Show interesting patterns in spending"""
        if len(self.expenses) < 2:
            print("\n📉 Need more data to show patterns!")
            return
        
        print("\n" + "="*50)
        print("🔍 SPENDING PATTERNS")
        print("="*50)
        
        # Most expensive category
        category_totals = {}
        for expense in self.expenses:
            cat = expense["category"]
            category_totals[cat] = category_totals.get(cat, 0) + expense["amount"]
        
        if category_totals:
            max_cat = max(category_totals, key=category_totals.get)
            max_amount = category_totals[max_cat]
            print(f"💰 Highest spending: {max_cat} (${max_amount:.2f})")
            
            min_cat = min(category_totals, key=category_totals.get)
            min_amount = category_totals[min_cat]
            print(f"💸 Lowest spending: {min_cat} (${min_amount:.2f})")
        
        # Average expense
        avg_expense = sum(e["amount"] for e in self.expenses) / len(self.expenses)
        print(f"📊 Average expense: ${avg_expense:.2f}")
        
        # Most expensive single purchase
        max_expense = max(self.expenses, key=lambda x: x["amount"])
        print(f"🎯 Most expensive: ${max_expense['amount']:.2f} ({max_expense['description']})")
        
        # Cheapest purchase
        min_expense = min(self.expenses, key=lambda x: x["amount"])
        print(f"🎯 Cheapest: ${min_expense['amount']:.2f} ({min_expense['description']})")
        
        # Monthly estimate (if we have at least 7 days of data)
        dates = [datetime.strptime(e["date"], "%Y-%m-%d %H:%M") for e in self.expenses]
        if dates:
            date_range = (max(dates) - min(dates)).days + 1
            if date_range >= 7:
                daily_avg = sum(e["amount"] for e in self.expenses) / date_range
                monthly_est = daily_avg * 30
                print(f"📅 Estimated monthly: ${monthly_est:.2f}")
    
    def show_recent_expenses(self):
        """Show recent expenses"""
        if not self.expenses:
            print("\n📭 No expenses to show!")
            return
        
        print("\n" + "="*50)
        print("📝 RECENT EXPENSES")
        print("="*50)
        
        # Show last 10 expenses
        recent = sorted(self.expenses, key=lambda x: x["date"], reverse=True)[:10]
        
        for expense in recent:
            color = expense.get("color", "")
            print(f"{color}${expense['amount']:8.2f} - {expense['category']:15} - {expense['description']:20} - {expense['date']}{self.reset_color}")
    
    def delete_expense(self):
        """Delete an expense"""
        self.show_recent_expenses()
        
        if not self.expenses:
            return
        
        try:
            expense_id = int(input("\nEnter expense ID to delete (or 0 to cancel): "))
            if expense_id == 0:
                return
            
            # Find and remove
            for i, expense in enumerate(self.expenses):
                if expense["id"] == expense_id:
                    removed = self.expenses.pop(i)
                    print(f"🗑️ Deleted: ${removed['amount']:.2f} for {removed['description']}")
                    self.save_data()
                    return
            
            print("❌ Expense ID not found!")
        except ValueError:
            print("❌ Please enter a valid ID!")
    
    def generate_summary(self):
        """Generate a text summary"""
        if not self.expenses:
            return "No expenses recorded yet!"
        
        total = sum(e["amount"] for e in self.expenses)
        avg = total / len(self.expenses)
        
        category_totals = {}
        for expense in self.expenses:
            cat = expense["category"]
            category_totals[cat] = category_totals.get(cat, 0) + expense["amount"]
        
        max_cat = max(category_totals, key=category_totals.get) if category_totals else "None"
        
        summary = f"""
💰 EXPENSE SUMMARY
==================
Total Spent: ${total:.2f}
Number of Expenses: {len(self.expenses)}
Average per Expense: ${avg:.2f}
Highest Spending Category: {max_cat}
Date Range: {min(e['date'] for e in self.expenses)} to {max(e['date'] for e in self.expenses)}

Category Breakdown:
"""
        for category, amount in sorted(category_totals.items()):
            percentage = (amount / total) * 100
            summary += f"  {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        return summary
    
    def export_summary(self):
        """Export summary to file"""
        summary = self.generate_summary()
        filename = f"expense_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        with open(filename, 'w') as f:
            f.write(summary)
        
        print(f"📄 Summary exported to: {filename}")
    
    def show_menu(self):
        """Display main menu"""
        while True:
            print("\n" + "="*50)
            print("💰 PERSONAL EXPENSE VISUALIZER")
            print("="*50)
            print("1. ➕ Add Expense")
            print("2. 📊 View Chart")
            print("3. 🔍 View Patterns")
            print("4. 📝 View Recent")
            print("5. 🗑️ Delete Expense")
            print("6. 📄 Export Summary")
            print("7. 💡 Tips to Save Money")
            print("8. 🚪 Exit")
            print("-"*50)
            
            try:
                choice = int(input("Choose option (1-8): "))
                
                if choice == 1:
                    self.add_expense()
                elif choice == 2:
                    self.show_ascii_chart()
                elif choice == 3:
                    self.show_spending_patterns()
                elif choice == 4:
                    self.show_recent_expenses()
                elif choice == 5:
                    self.delete_expense()
                elif choice == 6:
                    self.export_summary()
                elif choice == 7:
                    self.show_money_tips()
                elif choice == 8:
                    print("\n💾 Saving data...")
                    self.save_data()
                    print("👋 Goodbye! See you next time!")
                    break
                else:
                    print("❌ Please choose 1-8")
            
            except ValueError:
                print("❌ Please enter a number!")
    
    def show_money_tips(self):
        """Show random money-saving tips"""
        tips = [
            "💡 Track every expense for 30 days to understand spending habits",
            "💡 Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings",
            "💡 Wait 24 hours before making non-essential purchases",
            "💡 Unsubscribe from marketing emails to reduce impulse buying",
            "💡 Cook at home 1 more time per week to save on food costs",
            "💡 Use cash instead of cards for discretionary spending",
            "💡 Review subscriptions monthly - cancel what you don't use",
            "💡 Buy generic brands for everyday items",
            "💡 Plan meals for the week before grocery shopping",
            "💡 Use public transport or carpool to save on fuel"
        ]
        
        print("\n" + "="*50)
        print("💡 MONEY SAVING TIPS")
        print("="*50)
        print(random.choice(tips))
        print("\nMore tips:")
        for i, tip in enumerate(random.sample(tips, 3), 1):
            print(f"{i}. {tip}")

def main():
    """Main function"""
    print("\n" + "="*50)
    print("💰 WELCOME TO PERSONAL EXPENSE VISUALIZER")
    print("="*50)
    print("Track, visualize, and understand your spending habits!")
    
    visualizer = ExpenseVisualizer()
    visualizer.show_menu()

if __name__ == "__main__":
    main()