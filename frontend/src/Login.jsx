
function Login(){
  return (
    <div class="container vh-100 d-flex justify-content-center align-items-center">
        <div class="row w-100 justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="card p-4">
                    <div class="card-body">
                        <h3 class="text-center mb-4">Login</h3>
                        <form>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email address</label>
                                <input class="form-control" id="email" placeholder="name@example.com" required />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" placeholder="Enter password" required />
                            </div>
                            <div class="mb-3 form-check d-flex justify-content-between">
                                <div>
                                    <input type="checkbox" class="form-check-input" id="rememberMe" />
                                    <label class="form-check-label" for="rememberMe">Remember me</label>
                                </div>
                                <a href="#" class="text-decoration-none">Forgot password?</a>
                            </div>
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary">Sign In</button>
                            </div>
                        </form>
                        <hr class="my-4" />
                        <p class="text-center mb-0">Don't have an account? <a href="#" class="text-decoration-none">Register</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Login