from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password ,check_password
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Product,Category,Customer,Order
from django.contrib.auth import logout


class IndexView(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_category()
        categoryID = request.GET.get('category')

        if categoryID:
            products = Product.get_all_product_by_id(categoryID)
        else:
            products = Product.get_all_product()

        data = {
            'products': products,
            'categories': categories,
        }

        return render(request, 'Store/index.html', data)

    def post(self, request):
        # Retrieve the 'product' data from the POST request
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        
        cart = request.session.get('cart',{})

        if cart:
            quantity = cart.get(product,0)
            if remove:
                if quantity <= 1:
                    cart.pop(product)
                else:
                    cart[product] = quantity - 1
                
            else:
                cart[product] = 1 + quantity
        else:
            cart = {product: 1}

        request.session['cart'] = cart
        print("cart", request.session['cart'])

        # Redirect to the same page or another page based on the processing result
        return redirect('index')




class SigninView(View):
    template_name = 'Store/signin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        usertype_str = request.POST.get('usertype', 'False')
        usertype = usertype_str.lower() == 'true' 

        values = {
            'name': name,
            'email': email,
            'phone_no': phone_no
        }

        error_msg = self.validate_customer(name, email, phone_no, password)

        if not error_msg:
            customer = Customer(
                name=name,
                email=email,
                phone_no=phone_no,
                password=password,
                usertype=usertype,
            )
            customer.password = make_password(customer.password)
            customer.register()
            if usertype:
                return redirect('company')   
            else:
                return redirect('index')
        else:
            data = {
                'values': values,
                'error_msg': error_msg
            }
            return render(request, self.template_name, data)

    def validate_customer(self, name, email, phone_no, password):
        error_msg = None

        if not name:
            error_msg = "Name is required"
        elif not email:
            error_msg = "Email is required"
        elif not phone_no:
            error_msg = "Phone number is required"
        elif not self.is_valid_phone(phone_no):
            error_msg = "Invalid phone number"
        elif not password:
            error_msg = "Password is required"
        elif Customer.isExistEmail(email):
            error_msg = "Email is already taken"

        return error_msg

    def is_valid_phone(self, phone_no):
        return len(phone_no) == 10 and phone_no.isdigit()
    
    
    
class LoginView(View):
    template_name = 'Store/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        entereduser_str = request.POST.get('usertype', 'False')
        entereduser = entereduser_str.lower() == 'true' 
        customer = Customer.getCustomerByEmail(email)
        # print(entereduser ^ customer.usertype)
        # return HttpResponse("hi")
        error_msg = None

        if customer:
            if check_password(password, customer.password):
                
                if entereduser == customer.usertype:
                    request.session['customer'] = customer.id
                    request.session['email'] = customer.email
                    request.session['usertpye'] = customer.usertype
                    
                    if entereduser:
                        return redirect('company')
                    else:
                        return redirect('index')
                else:
                    error_msg = "usertype is invalid"
                                
                
                
            else:
                error_msg = "Email or password is invalid"
        else:
            error_msg = "Email or password is invalid"

        return render(request, self.template_name, {'error_msg': error_msg})
        
        


def LogOut(request):
    logout(request)
    return redirect('index')


class CartView(View):
    def get(self, request):
        cart = request.session.get('cart')

        if cart:
            # Convert valid string IDs to integers
            try:
                ids = [int(product_id) for product_id in cart.keys() if product_id.isdigit()]
            except ValueError as e:
                # Handle the error (e.g., log it, print it, or handle it in another way)
                print(f"Error converting product IDs: {e}")
                ids = []
            
            products = Product.get_product_id(ids)
            print(products)
            return render(request, 'Store/cart.html', {'product': products})
        else:
            # Handle the case when 'cart' is not in the session or is None
            return render(request, 'Store/cart.html', {'product': []})



    def post(self, request):
        # Your post method logic here
        return render(request, 'Store/cart.html', {})



# class CheckOutView(View):
#     def post(self,request):
#         full_name = request.POST.get('fullName')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         cart = request.session.get('cart')
#         products = Product.get_all_product_by_id(list(cart.keys()))
#         customer = request.session.get('customer')
#         if not request.user.is_authenticated:
#             return redirect('login') 
        
#         for product in products:
#                 order = Order(
#                     customer=Customer(id=customer),
#                     product=product,
#                     price = product.Price,
#                     address=address,
#                     phone=phone,
#                     quantity=cart.get(str(product.id), 0)
#                 )
#                 order.placeOrder()
#         request.session['cart'] = {}
#         print(full_name,phone,address,email,customer,products)
#         return redirect('index')

class CheckOutView(View):
    def post(self, request):
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        products = Product.get_all_product_by_id(list(cart.keys()))
        customer = request.session.get('customer')

        # Create or get the customer instance

        customer_instance, created = Customer.objects.get_or_create(id=customer, defaults={'name': full_name, 'email': email})

        for product in products:
            order = Order(
                customer=customer_instance,
                product=product,
                price=product.Price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id), 0)
            )
            order.placeOrder()

        request.session['cart'] = {}
        print(full_name, phone, address, email, customer, products)
        return redirect('index')
    
    
# views.py


# from auth 


class ordersView(View):
    # Assuming you have a Customer object associated with the logged-in user
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.objects.filter(customer=customer).order_by('date')
        # orders = orders.reverse()
        return render(request, 'Store/orders.html', {'orders': orders})




class Company(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'Store/company.html', {'categories': categories})

    def post(self, request):
        Name = request.POST.get('Name')
        Price = request.POST.get('Price')
        Description = request.POST.get('Description')
        category_id = request.POST.get('category')  # Get the category ID from the form
        img = request.FILES.get('img')

        try:
            category = Category.objects.get(pk=category_id)  # Retrieve the Category instance using the ID
        except Category.DoesNotExist:
            category = None  # Handle the case where the category with the given ID does not exist

        product = Product(
            Name=Name,
            Price=Price,
            Description=Description,
            category=category,  # Assign the Category instance, not the ID
            img=img,
        )

        product.save()
        return HttpResponse("succes")
