require 'uri'

class Company < ActiveRecord::Base
  has_many :users

  attr_accessible :name, :logo, :logo_file_name, :logo_content_type, :logo_file_size, :logo_updated_at, :website, :email, :facebook_url, :twitter_handle, :year_founded, :industry, :company_type

  validates :name, presence: true, uniqueness: true
  validates_format_of :website, with: URI::regexp(%w(http https)), allow_blank: true, message: "is not a valid HTTP or HTTPS URL"
  validates_format_of :email, with: /\A([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})\Z/i, allow_blank: true
  validates_format_of :facebook_url, with: URI::regexp(%w(http https)), allow_blank: true, message: "is not a valid HTTP or HTTPS URL"
  validates_format_of :twitter_handle, with: /@([A-Za-z0-9_]{1,15})/, allow_blank: true, message: "is not a valid Twitter handle beginning with '@'"
  validates :year_founded, numericality: { only_integer: true }, allow_blank: true

  has_attached_file :logo,  :default_url => ActionController::Base.helpers.asset_path('missing-logo.png')
  
  def twitter_url
    "http://www.twitter.com/" + self.twitter_handle 
  end

end
