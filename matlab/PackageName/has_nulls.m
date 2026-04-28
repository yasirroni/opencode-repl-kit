function result = has_nulls(data, column)
    % has_nulls - Check if data contains null (NaN) values.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %
    % Returns:
    %   true if any NaN values exist, false otherwise.

    if isempty(data)
        result = false;
        return;
    end

    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end

    result = any(isnan(values));
end
