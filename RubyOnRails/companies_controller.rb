class CompaniesController < ApplicationController
  before_filter :current_user_or_guest
  before_filter :user_can_edit_company_filter, except: :show

  def show
    if params[:id]
      @company = Company.find(params[:id])
    end
  end
  
  def edit
    if params[:id]
      @company = Company.find(params[:id])
    end
  end

  def update
    @company = Company.find(params[:id])
    if @company.update_attributes(params[:company])
      flash[:success] = "Company profile updated."
      redirect_to @company
    else
      render 'edit'
    end
  end

  def upload
    if params[:id]
      @company = Company.find(params[:id])
      file = params[:qqfile]
      @company.logo = file
      if @company.save
        render :json => { :success => true, :filepath => @company.logo.url }
      else
        render :json => { :success => false, :error => "not implemented", :preventRetry => true }
      end
    end
  end

  private
  
    def user_can_edit_company_filter
      if !current_user || 
         !CompaniesHelper::user_can_edit_company(current_user, Company.find(params[:id]))
        redirect_to(root_url)
      end
    end
end
