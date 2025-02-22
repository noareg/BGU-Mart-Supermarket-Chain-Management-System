from persistence import *

import sys

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            
            product_id, quantity, activator_id, date = splittedline
            quantity = int(quantity)
            product=repo.products.find(id=product_id)
            if product: 
                product = product[0]  
            if quantity<0 :
                if product.quantity + quantity >=0:
                    new_quantity = product.quantity + quantity
                    repo.products.delete(id=product.id)
                    repo.products.insert(Product(product_id, product.description, product.price, new_quantity))
                    repo.activities.insert(Activitie(int(product_id), int(quantity), int(activator_id), date))
            elif quantity>0 :
                new_quantity = product.quantity + quantity
                repo.products.delete(id=product.id)
                repo.products.insert(Product(product_id, product.description, product.price, new_quantity))
                repo.activities.insert(Activitie(int(product_id), int(quantity), int(activator_id), date))

if __name__ == '__main__':
    main(sys.argv)