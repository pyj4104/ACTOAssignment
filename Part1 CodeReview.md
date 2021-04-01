# Original Code

``` php
class UserController
{
	public function update(Request $request)
	{
		if ($user->isAdmin()) {

			if (request(‘‘mark_as_active’’)) {		
				$user = User::find($request->get(‘user_id’));
				$user->active = true;
				$user->save();		
			} elseif ( request(“‘mark_as_inactiveactive’”) ) {
				$user = User::find($request->get(‘user_id’));
				$user->active = false;
				$user->save();
			} elseif (request(‘first_name’)) {
				$user->first_name = $request->get(‘first_name’);
				$user->last_name = $request->get(‘last_name’);
				$user->address = $request->get(‘address’);
				$user->save();
			} 

			return redirect()->back();

		} else {
			abort(400, “you do not have access”);
		}
	}
}
```

# About $user
1. `$user` is not defined, so the function will error out. Make sure to declare it first.
2. `$user->save()` is alway called. Put it outside of the if...then block.
3. It looks better to abort early if the `$user` is not an admin.
4. What would happen if the `$request` does not have 'user_id' variable. Make sure to take care of the error.
5. Be consistent with your code. Choose ' or '' or " and stick with one of them. (Is '' even allowed?)
6. What would happen if the request marks a user either active/inactive **AND** change the values. Checking request for first name should be in another if statement.
7. Check the documentation for the Request class. Why do you use $request->get() sometimes and not the other?

# Refactored Code

In the end, it should look like this.

``` php
class UserController
{
	public function update(Request $request)
	{
		$user = User::find($request->get(‘user_id’))

		if (!($user->isAdmin())) {
			abort(400, "you do not have access");
		}

		if (request('mark_as_active')) {
			$user->active = true;
		} elseif ( request('mark_as_inactiveactive') ) {
			$user->active = false;
		}
		
		if (request('first_name')) {
			$user->first_name = $request->get(‘first_name’);
			$user->last_name = $request->get(‘last_name’);
			$user->address = $request->get(‘address’);
		}

		$user->save();

		return redirect()->back();

	}
}
```
